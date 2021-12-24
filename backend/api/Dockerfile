### Base Python Container ###
FROM python:3.10-slim-bullseye AS base

WORKDIR /app

FROM base AS apt-packages

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends git \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

### Python Dependency Container ###
FROM base AS build

COPY --from=apt-packages /usr/bin/git /usr/bin/git
COPY poetry.lock pyproject.toml ./

RUN python3 -m pip install -U --no-cache-dir pip poetry git+git://github.com/samuelcolvin/pydantic@master\#egg=pydantic \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction \
    && python3 -m pip cache purge

### Development Container ###
FROM build AS runtime

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "python3", "main.py"]
