FROM unit:python3.11

WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

COPY load-model.py /app/
ARG RUN_LOAD_MODEL=false
RUN if [ "$RUN_LOAD_MODEL" = "true" ]; then python load-model.py; fi

COPY config/nginx-config.json /docker-entrypoint.d/

ENV PYTHONUNBUFFERED 1

COPY ./app/ /app/