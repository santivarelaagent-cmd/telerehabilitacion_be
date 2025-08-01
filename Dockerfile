FROM python:3

ENV PYTHONUNBUFFERED=1
WORKDIR /usr/api

# Install system dependencies needed for compiling Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev \
    libev-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and upgrade pip
COPY requirements.txt /usr/api
RUN pip install --upgrade pip setuptools wheel

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy application code
COPY . /usr/api

# Expose port
EXPOSE 8000

# Start command using gunicorn
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "telerehabilitation_API.wsgi:application"]

RUN python manage.py makemigrations && python manage.py migrate && python create_superuser.py

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
