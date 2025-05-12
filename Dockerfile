FROM python:3.11.4-alpine

WORKDIR /app

ENV PYTHONWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV PATH=".PY/BIN/:$PATH"

RUN pip install --upgrade pip

COPY . /app

RUN pip install -r requirements.txt
