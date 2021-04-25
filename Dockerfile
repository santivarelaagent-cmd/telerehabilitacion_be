FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/api
# RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
COPY requirements.txt /usr/api
RUN pip install -r requirements.txt
COPY . /usr/api