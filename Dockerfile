FROM python:latest

ENV PYTHONIOENCODING utf-8
ENV TZ="Asia/Tokyo"
ENV LANG=C.UTF-8
ENV LANGUAGE=en_US:en_US

WORKDIR /work

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt