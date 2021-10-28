FROM ubuntu:20.04 AS base

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    python3.9-full \
    python3-pip

COPY setup.py ./

RUN python3.9 -m pip install .

COPY . ./

EXPOSE 5000

CMD ["python3.9", "main.py"]