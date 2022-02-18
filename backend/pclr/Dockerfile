##################
# POETRY INSTALL #
##################
FROM python:3.10-slim-bullseye AS poetry-install

ENV POETRY_HOME /opt/poetry
ENV PATH $POETRY_HOME/bin:$PATH

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends curl \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python3 -

RUN poetry --version

########
# BASE #
########
FROM python:3.10-slim-bullseye AS project-deps

WORKDIR /app

ENV POETRY_HOME /opt/poetry
ENV VENV_PATH /app/venv
ENV PATH $POETRY_HOME/bin:$VENV_PATH/bin:$PATH

COPY --from=poetry-install $POETRY_HOME $POETRY_HOME
COPY poetry.lock pyproject.toml ./

RUN poetry --version

# Install Tooling
# Build-Essential -> required for installing project deps
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends build-essential \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Setup project
# 1. Start venv at VENV_PATH; --copies option will copy libs/binaries instead of links
# 2. Activate virtualenv
# 3. Install dependencies
RUN python -m venv --copies $VENV_PATH \
    poetry config virtualenvs.create false \
    && . $VENV_PATH/bin/activate \
    && poetry install --no-root --no-dev --no-interaction

###########
# RUNTIME #
###########
FROM python:3.10-slim-bullseye AS runtime

# Pull virtualenv from base image
COPY --from=project-deps /app/venv /app/venv

ENV PATH /app/venv/bin:$PATH

WORKDIR /app

COPY . .

CMD ["python", "main.py"]
