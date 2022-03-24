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

### BASE ###
FROM python:3.10-slim-bullseye AS base

WORKDIR /app

ENV POETRY_HOME /opt/poetry
ENV VENV_PATH /app/venv
ENV PATH $POETRY_HOME/bin:$VENV_PATH/bin:$PATH

COPY --from=poetry-install $POETRY_HOME $POETRY_HOME
COPY poetry.lock pyproject.toml ./

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends build-essential \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv --copies $VENV_PATH \
    poetry config virtualenvs.create false \
    && . $VENV_PATH/bin/activate \
    && poetry install --no-root --no-dev --no-interaction

### Python Dependency Container ###
FROM python:3.10-slim-bullseye AS runtime

COPY --from=base /app/venv /app/venv

ENV PATH /app/venv/bin:$PATH

WORKDIR /app

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
