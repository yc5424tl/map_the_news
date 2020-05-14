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
apt-get install software-properties-common -y && \
add-apt-repository ppa:ubuntugis/ppa -y && \
apt-get update && \
apt-get install -y \
    curl
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
export CPLUS_INCLUDE_PATH=/usr/include/gdal &&
export C_INCLUDE_PATH=/usr/include/gdal &&
pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["/bin/bash", "-c", "./entrypoint.sh"]