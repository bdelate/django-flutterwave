# Pull base image
FROM python:3.7.3

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Upgrade pip and install poetry
RUN pip install --upgrade pip
RUN pip install poetry

# Set work directory
WORKDIR /code

# Copy project into container
COPY . .

WORKDIR /code/example

RUN poetry install