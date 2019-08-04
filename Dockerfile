FROM python:3.7.3-slim-stretch
LABEL maintainer="me@wolfbolin.com"

WORKDIR /var/app

COPY . /var/app/

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

CMD python src/web.py
