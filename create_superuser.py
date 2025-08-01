# create_superuser.py
import os
import django
import environ

environ.Env.read_env()
env = environ.Env()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telerehabilitation_API.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = env("DJANGO_SUPERUSER_USERNAME", default="admin")
email = env("DJANGO_SUPERUSER_EMAIL", default="admin@example.com")
password = env("DJANGO_SUPERUSER_PASSWORD", default="123456789")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superuser '{username}' creado con contraseña '{password}'")
else:
    print(f"El superuser '{username}' ya existe.")