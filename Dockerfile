FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /usr/api

# Instala herramientas de compilación y librerías necesarias para psycopg2, gevent, etc.
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libev-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /usr/api

# Mejores prácticas: actualizar pip y herramientas de compilación
RUN pip install --upgrade pip setuptools wheel

# Instala dependencias
RUN pip install -r requirements.txt

COPY . /usr/api