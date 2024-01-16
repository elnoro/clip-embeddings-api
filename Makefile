build/slim:
	docker build . -t ghcr.io/elnoro/clip-embeddings-api:v0-slim --target prod

publish/slim: build/slim
	docker push ghcr.io/elnoro/clip-embeddings-api:v0-slim

build/preloaded:
	docker build . --build-arg RUN_LOAD_MODEL=true -t ghcr.io/elnoro/clip-embeddings-api:v0-preloaded --target=prod

test:
	PYTHONPATH="${PYTHONPATH}:/app" pytest

testC:
	docker compose exec app make test

lint:
	black . --check

lintC:
	docker compose exec app make lint

check: lint test

checkC:
	docker compose exec app make check