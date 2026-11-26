import re
import unicodedata


def strip_accents(text):
    """Normaliza a minúsculas y elimina tildes/diacríticos (á->a, ñ->n, ü->u)."""
    if not text:
        return ''
    normalized = unicodedata.normalize('NFD', str(text).lower())
    return ''.join(ch for ch in normalized if unicodedata.category(ch) != 'Mn')


def spanish_phonetic(text):
    """
    Normalización fonética pensada para español y errores comunes de dislexia:
    - Ignora tildes y mayúsculas
    - Unifica sonidos equivalentes: b/v, s/z/c(e,i), g(e,i)/j, ll/y, k/qu/c(a,o,u), h muda
    - Colapsa letras repetidas consecutivas (ej. 'rodiilla' -> 'rodila')
    """
    s = strip_accents(text)
    s = re.sub(r'[^a-z0-9\s]', ' ', s)
    # Equivalencias fonéticas en español
    s = s.replace('ll', 'y')
    s = s.replace('qu', 'k')
    s = re.sub(r'c(?=[ei])', 's', s)
    s = re.sub(r'c(?=[aou])', 'k', s)
    s = re.sub(r'g(?=[ei])', 'j', s)
    s = s.replace('v', 'b')
    s = s.replace('z', 's')
    s = s.replace('h', '')
    s = s.replace('x', 'ks')
    # Colapsar letras repetidas consecutivas (ej. rr -> r, oo -> o)
    s = re.sub(r'([a-z])\1+', r'\1', s)
    return re.sub(r'\s+', ' ', s).strip()


def damerau_levenshtein(a, b, max_dist=2):
    """
    Distancia Damerau-Levenshtein acotada:
    Cuenta inserciones, eliminaciones, sustituciones y transposiciones adyacentes
    (ej. 'hmobro' <-> 'hombro' = distancia 1).
    """
    if a == b:
        return 0
    len_a, len_b = len(a), len(b)
    if abs(len_a - len_b) > max_dist:
        return max_dist + 1
    if len_a == 0:
        return len_b
    if len_b == 0:
        return len_a

    # Matriz de DP
    d = [[0] * (len_b + 1) for _ in range(len_a + 1)]
    for i in range(len_a + 1):
        d[i][0] = i
    for j in range(len_b + 1):
        d[0][j] = j

    for i in range(1, len_a + 1):
        row_min = max_dist + 1
        ca = a[i - 1]
        for j in range(1, len_b + 1):
            cb = b[j - 1]
            cost = 0 if ca == cb else 1
            val = min(
                d[i - 1][j] + 1,       # eliminación
                d[i][j - 1] + 1,       # inserción
                d[i - 1][j - 1] + cost # sustitución
            )
            if i > 1 and j > 1 and ca == b[j - 2] and a[i - 2] == cb:
                val = min(val, d[i - 2][j - 2] + 1)  # transposición adyacente
            d[i][j] = val
            if val < row_min:
                row_min = val
        if row_min > max_dist:
            return max_dist + 1

    return d[len_a][len_b]


def _allowed_distance(token_len):
    if token_len <= 2:
        return 0
    if token_len <= 4:
        return 1
    if token_len <= 8:
        return 2
    return 3


def _token_matches_text(token_clean, token_phon, target_clean, target_words, target_phon, target_phon_words):
    # 1) Subcadena exacta normalizada (sin tildes ni mayúsculas)
    if token_clean in target_clean:
        return True

    # 2) Subcadena fonética (ej. 'rodiya' -> 'rodilla', 'ombro' -> 'hombro', 'mobilidad' -> 'movilidad')
    if token_phon and len(token_phon) >= 2 and token_phon in target_phon:
        return True

    max_dist = _allowed_distance(len(token_clean))
    if max_dist == 0:
        return False

    # 3) Coincidencia difusa (Damerau-Levenshtein) contra cada palabra o prefijo del texto
    for word in target_words:
        if len(word) < 2:
            continue
        if damerau_levenshtein(token_clean, word, max_dist) <= max_dist:
            return True
        # También permitir coincidencia difusa contra prefijo de palabra larga (mientras escribe)
        if len(word) > len(token_clean) >= 4:
            prefix = word[:len(token_clean)]
            if damerau_levenshtein(token_clean, prefix, min(max_dist, 1)) <= min(max_dist, 1):
                return True

    # 4) Coincidencia difusa sobre la versión fonética (ej. 'lumbal' -> 'lumbar', 'abudcsion' -> 'abduccion')
    if token_phon and len(token_phon) >= 3:
        phon_max = _allowed_distance(len(token_phon))
        for pword in target_phon_words:
            if len(pword) < 2:
                continue
            if damerau_levenshtein(token_phon, pword, phon_max) <= phon_max:
                return True

    return False


def filter_queryset_fuzzy(qs, search_text, fields=('name', 'description')):
    """
    Filtra un QuerySet usando búsqueda tolerante a dislexia, tildes, fonética española
    y errores tipográficos sobre los campos indicados (además del ID si es numérico).
    """
    raw_query = (search_text or '').strip()
    if not raw_query:
        return qs

    clean_query = re.sub(r'[^a-z0-9\s]', ' ', strip_accents(raw_query))
    tokens = [t for t in clean_query.split() if t]
    if not tokens:
        return qs

    prepared_tokens = [(t, spanish_phonetic(t)) for t in tokens]
    numeric_id = int(raw_query) if raw_query.isdigit() else None

    matching_ids = []
    for row in qs.values_list('id', *fields):
        row_id = row[0]
        if numeric_id is not None and row_id == numeric_id:
            matching_ids.append(row_id)
            continue

        combined = ' '.join(str(val or '') for val in row[1:])
        target_clean = re.sub(r'[^a-z0-9\s]', ' ', strip_accents(combined))
        target_words = target_clean.split()
        target_phon = spanish_phonetic(combined)
        target_phon_words = target_phon.split()

        if all(
            _token_matches_text(tc, tp, target_clean, target_words, target_phon, target_phon_words)
            for tc, tp in prepared_tokens
        ):
            matching_ids.append(row_id)

    return qs.filter(id__in=matching_ids)
