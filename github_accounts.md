# Guía: Configurar Múltiples Cuentas de GitHub

Esta guía te permite trabajar con múltiples cuentas de GitHub en el mismo equipo y cambiar entre ellas fácilmente.

## 📋 Requisitos Previos

- Git instalado
- GitHub CLI (`gh`) instalado
  - Descargar desde: https://cli.github.com/
  - O instalar con winget: `winget install --id GitHub.cli`

---

## 🚀 Configuración Inicial (Primera Vez)

### 1. Autenticar la Primera Cuenta

```bash
# Autenticarse con la primera cuenta
gh auth login

# Seleccionar:
# - GitHub.com
# - HTTPS
# - Yes (authenticate Git with GitHub credentials)
# - Login with a web browser
```

Sigue las instrucciones en el navegador para autorizar GitHub CLI.

### 2. Autenticar Cuentas Adicionales

```bash
# Añadir una segunda cuenta
gh auth login

# Usar las mismas opciones
# El navegador te pedirá iniciar sesión con la otra cuenta
```

Repite este proceso para cada cuenta que necesites añadir.

### 3. Configurar Git para Usar GitHub CLI

```bash
# Esto es CRÍTICO: configura Git para usar gh como credential helper
gh auth setup-git
```

**¿Qué hace esto?**
- Configura Git para obtener credenciales desde GitHub CLI
- Elimina conflictos con credenciales cacheadas en Windows
- Sincroniza automáticamente con la cuenta activa de `gh`

### 4. Limpiar Credenciales Antiguas (Importante)

```bash
# Ver credenciales de git existentes
cmdkey /list | findstr git

# Si existe git:https://github.com, eliminarla:
cmdkey /delete:LegacyGeneric:target=git:https://github.com
```

---

## 🔄 Uso Diario: Cambiar Entre Cuentas

### Ver Cuentas Disponibles

```bash
gh auth status
```

**Salida ejemplo:**
```
github.com
  ✓ Logged in to github.com account cuenta1 (keyring)
  - Active account: true
  ...
  ✓ Logged in to github.com account cuenta2 (keyring)
  - Active account: false
  ...
```

### Cambiar de Cuenta

```bash
# Cambiar a otra cuenta
gh auth switch -u nombre-de-cuenta

# Verificar el cambio
gh auth status
```

### Trabajar con Git

```bash
# Después de hacer switch, usar Git normalmente
git clone https://github.com/usuario/repo.git
git pull
git push origin main

# Git automáticamente usará la cuenta activa de gh
```

---

## 🛠️ Solución de Problemas

### Error 403: Permission Denied

**Causa:** Git está usando credenciales cacheadas incorrectas.

**Solución:**
```bash
# 1. Ver credenciales guardadas
cmdkey /list | findstr git

# 2. Eliminar credencial problemática
cmdkey /delete:LegacyGeneric:target=git:https://github.com

# 3. Reconfigurar credential helper
gh auth setup-git

# 4. Intentar de nuevo
git push origin main
```

### Verificar Configuración de Git

```bash
# Ver qué credential helper está activo
git config --global credential.helper

# Debería mostrar algo como:
# !C:/Program Files/GitHub CLI/gh.exe auth git-helper
```

### Push/Pull Usa la Cuenta Incorrecta

```bash
# Verificar cuenta activa
gh auth status

# Cambiar a la cuenta correcta
gh auth switch -u cuenta-correcta

# Intentar la operación de nuevo
git push origin main
```

---

## 📝 Ejemplo de Flujo de Trabajo

### Proyecto con Cuenta Personal

```bash
# 1. Cambiar a cuenta personal
gh auth switch -u mi-cuenta-personal

# 2. Clonar repositorio
git clone https://github.com/mi-cuenta-personal/mi-proyecto.git

# 3. Trabajar normalmente
cd mi-proyecto
git add .
git commit -m "Cambios"
git push origin main
```

### Proyecto con Cuenta de Trabajo

```bash
# 1. Cambiar a cuenta de trabajo
gh auth switch -u mi-cuenta-trabajo

# 2. Clonar repositorio de trabajo
git clone https://github.com/empresa/proyecto-trabajo.git

# 3. Trabajar normalmente
cd proyecto-trabajo
git add .
git commit -m "Feature"
git push origin main
```

---

## ⚙️ Configuración Avanzada

### Configurar Git por Repositorio (Opcional)

Si prefieres configurar nombre y email específicos por repositorio:

```bash
# Dentro del repositorio
git config user.name "Nombre Específico"
git config user.email "email@especifico.com"

# Ver configuración local
git config --local --list
```

### Usar SSH en Lugar de HTTPS (Alternativa)

Si prefieres SSH, necesitas:

1. **Generar claves SSH para cada cuenta:**
```bash
# Cuenta 1
ssh-keygen -t ed25519 -C "email1@ejemplo.com" -f ~/.ssh/id_ed25519_cuenta1

# Cuenta 2
ssh-keygen -t ed25519 -C "email2@ejemplo.com" -f ~/.ssh/id_ed25519_cuenta2
```

2. **Configurar SSH config** (`~/.ssh/config`):
```
Host github.com-cuenta1
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_cuenta1

Host github.com-cuenta2
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_cuenta2
```

3. **Clonar con alias SSH:**
```bash
git clone git@github.com-cuenta1:usuario/repo.git
```

---

## ✅ Checklist de Configuración

- [ ] GitHub CLI instalado (`gh --version`)
- [ ] Primera cuenta autenticada (`gh auth login`)
- [ ] Cuentas adicionales autenticadas
- [ ] Git configurado para usar gh (`gh auth setup-git`)
- [ ] Credenciales antiguas eliminadas (`cmdkey /delete...`)
- [ ] Verificar que funciona (`gh auth status` y `git push`)

---

## 🔗 Referencias

- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [Git Credential Manager](https://github.com/git-ecosystem/git-credential-manager)
- [GitHub Multiple Accounts Guide](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github)

---

## 💡 Consejos

1. **Siempre verifica la cuenta activa** antes de hacer push a repositorios importantes
2. **Usa `gh auth status`** frecuentemente para confirmar qué cuenta estás usando
3. **No uses `git config --global user.name/email`** si trabajas con múltiples cuentas; configúralo por repositorio
4. **GitHub CLI maneja los tokens automáticamente**, no necesitas copiar/pegar tokens manualmente

---

**Última actualización:** Octubre 2025