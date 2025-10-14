#!/bin/sh
set -e

echo "📌 Ejecutando migraciones..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "📌 Cargando datos iniciales..."
python manage.py loaddata initial_data.json || echo "⚠️ No se pudieron cargar los fixtures (puede que ya estén cargados)"

echo "📌 Creando superusuario si no existe..."
python create_superuser.py || echo "⚠️ No se creó superusuario (puede que ya exista)"

echo "🚀 Iniciando servidor Django..."
python manage.py runserver 0.0.0.0:8000
