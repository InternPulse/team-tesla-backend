# Use an official Python runtime as a parent image
FROM python:3.10-slim

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1

RUN apt-get update -qq

# Install Python 3.6 and python3-venv
RUN apt-get install python3 python3-dev python3-pip python3-venv -y

# Install required system dependencies
RUN apt-get install -yqq \
    libproj-dev \
    gdal-bin \
    memcached \
    libmemcached-dev \
    build-essential \
    git \
    libcurl4-openssl-dev \
    libssl-dev \
    libpq-dev \
    gfortran \
    libatlas-base-dev \
    libjpeg-dev \
    libxml2-dev \
    libxslt-dev \
    zlib1g-dev \
    software-properties-common \
    ghostscript \
    libpcre3 \
    libpcre3-dev \
    python3-celery \
    python3-sphinx \
    locales \
    pkg-config \
    gcc \
    libtool \
    nano \
    sudo \
    automake
# Set the working directory to /team-tesla-backend
WORKDIR /team-tesla-backend

# Copy the current directory contents into the container at /team-tesla-backend
COPY . /team-tesla-backend

# Install any needed packages specified in requirements.txt
COPY requirements.txt /team-tesla-backend/requirements.txt

RUN    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install django
