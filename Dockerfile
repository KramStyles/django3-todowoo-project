FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1

LABEL Karm Designs

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .

CMD [ "django", "r", "5000" ]