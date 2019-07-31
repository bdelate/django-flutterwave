# Pull base image
FROM python:3.7.3

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

COPY . .

# Upgrade pip and install poetry
RUN pip install --upgrade pip
RUN pip install poetry


# copy dependencies into container and install them
# COPY pyproject.toml .
# COPY poetry.lock .

# build poetry
RUN poetry build
RUN poetry install

# Copy local project code into container
# Set work directory
WORKDIR /code/djangorave/example
# COPY ./djangorave/ .