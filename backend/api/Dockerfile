### Base Python Container ###
FROM python:3.10-slim AS base

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install git -y

FROM base AS python-deps

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN python3 -m pip install -U pip poetry git+git://github.com/samuelcolvin/pydantic@master#egg=pydantic
RUN poetry config virtualenvs.create false \
    && poetry install

### Development Container ###
FROM python-deps AS dev

COPY . ./

EXPOSE 5000

CMD ["poetry", "run", "python3", "main.py"]

### Test Container ###
FROM dev AS test

CMD ["poetry", "run", "pytest"]

