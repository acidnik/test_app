FROM python:3.7.4-alpine3.10

RUN apk add --no-cache python3 gcc musl-dev python3-dev postgresql-dev

# если сначала копировать только requirements.txt, то установка pip пакетов кешируется
COPY ./requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app

RUN pip3 install -r requirements.txt

COPY . /opt/app
