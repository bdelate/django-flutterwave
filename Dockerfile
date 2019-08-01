# Pull base image
FROM python:3.7.3

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Copy local project code into container
COPY . .

# Upgrade pip and install poetry
RUN pip install --upgrade pip
RUN pip install poetry

# build djangorave and install packages
RUN poetry build
RUN poetry install

# Set work directory to example
WORKDIR /code/example