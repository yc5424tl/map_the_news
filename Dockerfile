#!/bin/bash

FROM ubuntu:eoan-20200410
SHELL ["/bin/bash", "-c"]
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

COPY requirements.txt ./

RUN \
apt-get update && \
apt-get install -y \
    curl \
    python3 \
    python3-pip \
    gcc \
    gdal-bin \
    gdal-data \
    libgdal20 \
    libgdal-dev \
    python3.7-dev \
    python3-gdal \
    python3-rtree && \
pip3 install --global-option=build_ext --global-option="-I/usr/include/gdal" GDAL==2.4.2 && \
pip3 install -r requirements.txt


COPY . .

ENV SECRET_KEY=supserSecret123!

RUN \
python3 manage.py makemigrations mtn_web && \
python3 manage.py makemigrations mtn_user && \
python3 manage.py migrate mtn_web --noinput && \
python3 manage.py migrate mtn_user --noinput && \
python3 manage.py migrate sessions --noinput && \
python3 manage.py migrate admin --noinput

EXPOSE 8000

CMD ["/bin/bash", "-c", "./entrypoint.sh"]