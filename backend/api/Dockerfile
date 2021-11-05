FROM python:3.10-slim AS base

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends

RUN python3 -m pip install -U pip poetry

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install

COPY . ./

EXPOSE 5000

CMD ["poetry", "run", "python3", "main.py"]