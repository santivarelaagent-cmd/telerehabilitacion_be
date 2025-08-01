FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /usr/api

# Instala dependencias del sistema necesarias para compilar paquetes como psycopg2, greenlet, etc.
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /usr/api
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /usr/api