FROM python:3.8-slim-buster

LABEL Karm Designs

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "django", "r", "5000" ]