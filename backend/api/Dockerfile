FROM python:3.10-slim AS base

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN python3 -m pip install -U pip poetry

FROM base AS python-deps

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install

FROM python-deps AS dev

COPY . ./

EXPOSE 5000

CMD ["poetry", "run", "python3", "main.py"]