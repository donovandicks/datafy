### Base Python Container ###
FROM python:3.10-slim AS base

WORKDIR /app

FROM base AS deps

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends git \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

### Python Dependency Container ###
FROM deps AS python-deps

COPY poetry.lock pyproject.toml ./

RUN python3 -m pip install -U pip poetry git+git://github.com/samuelcolvin/pydantic@master\#egg=pydantic \
    && poetry config virtualenvs.create false \
    && poetry install

### Development Container ###
FROM python-deps AS dev

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "python3", "main.py"]

### Test Container ###
FROM dev AS test

CMD ["poetry", "run", "pytest"]
