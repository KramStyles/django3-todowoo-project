FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1

LABEL Karm Designs

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN django mm
RUN django m

EXPOSE 5000

COPY . .

CMD [ "django", "r", "5000" ]