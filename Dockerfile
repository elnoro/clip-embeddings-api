FROM unit:python3.11 as prod

WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

ENV MODEL_NAME="clip-ViT-B-32"
COPY load-model.py /app/
ARG RUN_LOAD_MODEL=false
RUN if [ "$RUN_LOAD_MODEL" = "true" ]; then python load-model.py; fi

COPY config/nginx-config.json /docker-entrypoint.d/

ENV PYTHONUNBUFFERED 1

COPY ./app/ /app/

FROM python:3.11 as dev

WORKDIR /app

COPY poetry.lock pyproject.toml /app/
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi
ENV MODEL_NAME="clip-ViT-B-32"
COPY load-model.py /app/
RUN python load-model.py

CMD [ "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0" ,"--port", "8000" ]