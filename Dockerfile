FROM python:3.8-slim as builder

ARG WORKDIR
WORKDIR ${WORKDIR}

COPY pyproject.toml poetry.lock src/ README.md ./

RUN pip install poetry && \
    poetry export -f requirements.txt > requirements.txt && \
    poetry build


FROM python:3.8-slim as prod

ARG WORKDIR
WORKDIR ${WORKDIR}

RUN apt-get update && \
    apt-get install -y git locales subversion && \
    echo "en_US UTF-8" > /etc/locale.gen && \
    locale-gen

COPY --from=builder ${WORKDIR}/requirements.txt ${WORKDIR}/dist/*.whl ./

RUN pip install -r requirements.txt && \
    pip install git_svn_monitor-0.1.0-py3-none-any.whl
