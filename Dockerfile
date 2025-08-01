FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /usr/api

# 1. Instala herramientas de compilación + headers de Debian
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpython3.11-dev \
    libpq-dev \
    libev-dev && \
    rm -rf /var/lib/apt/lists/*

# 1b. Asegura que gcc encuentre los headers en /usr/local/include
RUN mkdir -p /usr/local/include/python3.11 && \
    cp -r /usr/include/python3.11/* /usr/local/include/python3.11/

# 2. Copia requirements y actualiza pip
COPY requirements.txt /usr/api
RUN pip install --upgrade pip setuptools wheel

# 3. Instala dependencias (incluye ruamel.yaml.clib)
RUN pip install -r requirements.txt

# 4. Copia el código fuente
COPY . /usr/api