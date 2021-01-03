FROM python:3.7
ENV PYTHONUNBUFFERED=1 \
  POETRY_VERSION=1.0.9 \
  POETRY_VIRTUALENVS_CREATE=false \
  PIP_DISABLE_PIP_VERSION_CHECK=on
ARG IGNORE_DEV_DEPS


RUN mkdir /code
WORKDIR /code

RUN pip install "poetry==$POETRY_VERSION"
COPY poetry.lock pyproject.toml /code/
RUN poetry install --no-interaction --no-ansi --no-root


ADD . /code/
