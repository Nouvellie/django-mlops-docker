FROM python:3.9.6-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip setuptools

RUN useradd -ms /bin/bash main

USER main

WORKDIR /home/main

RUN python3 -m venv djangomlopsdocker

COPY --chown=main ./src/main/requirements /home/main/requirements/

RUN ./djangomlopsdocker/bin/pip3 install --upgrade pip

RUN ./djangomlopsdocker/bin/pip3 install -r /home/main/requirements/requirement.txt

COPY --chown=main ./src/main /home/main/