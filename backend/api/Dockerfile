FROM ubuntu:20.04 AS base

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    python3.9-full \
    python3-pip

RUN python3.9 -m pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install

COPY . ./

EXPOSE 5000

CMD ["poetry", "run", "python3.9", "main.py"]