#!/bin/bash

FROM ubuntu:eoan-20200410
SHELL ["/bin/bash", "-c"]
WORKDIR /

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG False

# COPY requirements.txt ./
COPY ./requirements.txt .

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

# COPY . .
ADD . .

EXPOSE 8000

# ENV HOME=/home/app
# RUN mkdir $APP_HOME/staticfiles

CMD ["/bin/bash", "-c", "./entrypoint.sh"]