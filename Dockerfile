#!/bin/bash

FROM ubuntu:eoan-20200410
SHELL ["/bin/bash", "-c"]
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

COPY requirements.txt ./

RUN apt-get update && \
apt-get install -y \
    python3 \
    python3-pip \
    gcc \
    libgdal20 \
    libgdal-dev \
    python3-gdal && \
apt update && \
apt install -y \
    gdal-bin \
    python-gdal \
    python3-gdal \
    python3-rtree \
    curl && \
pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["/bin/bash", "-c", "./entrypoint.sh"]