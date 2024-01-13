FROM unit:python3.11

WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

COPY load-model.py /app/
RUN python load-model.py

RUN chown -R unit:unit /app 

COPY config/nginx-config.json /docker-entrypoint.d/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./app/ /app/