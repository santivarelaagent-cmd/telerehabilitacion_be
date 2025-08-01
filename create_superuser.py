# create_superuser.py
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telerehabilitation_API.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "123456789")
    print("Superuser 'admin' creado con contraseña 123456789")
else:
    print("El superuser 'admin' ya existe.")