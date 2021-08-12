FROM python:3.8-slim as builder

WORKDIR /usr/src/app

RUN pip install poetry
COPY pyproject.toml poetry.lock src/ README.md ./

RUN poetry export -f requirements.txt > requirements.txt & \
    poetry build


FROM python:3.8-slim as dev

ENV PYTHONUNBUFFERED=1
ENV LANG=en_US.UTF-8

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y git subversion

COPY --from=builder /usr/src/app/requirements.txt /usr/src/app/dist/*.whl ./

RUN pip install -r requirements.txt && \
    pip install git_svn_monitor-0.1.0-py3-none-any.whl
