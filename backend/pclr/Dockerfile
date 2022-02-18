# BASE
# Installs all package dependencies
FROM python:3.10-slim-bullseye AS base

# Install Tooling
# 1. Curl -> required for installing poetry
# 2. Build-Essential -> required for installing project deps
# 3. Poetry -> required for installing the package
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends curl build-essential \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python -

# Poetry added to PATH
ENV PATH /root/.local/bin:$PATH
# Define a path for a virtualenv
ENV VENV_PATH=/app/venv

WORKDIR /app

COPY poetry.lock pyproject.toml ./

# Setup project
# 1. Start venv at VENV_PATH; --copies option will copy libs/binaries instead of links
# 2. Activate virtualenv
# 3. Install dependencies
RUN python -m venv --copies $VENV_PATH \
    poetry config virtualenvs.create false \
    && . $VENV_PATH/bin/activate \
    && poetry install --no-root --no-dev --no-interaction

# RUNTIME
FROM python:3.10-slim-bullseye AS RUNTIME

# Pull virtualenv from base image
COPY --from=base /app/venv /app/venv

ENV PATH /app/venv/bin:$PATH

WORKDIR /app

COPY . .

CMD ["python", "pclr/main.py"]
