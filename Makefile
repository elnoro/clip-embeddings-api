build/slim:
	docker build . -t ghcr.io/elnoro/clip-embeddings-api:v0-slim

publish/slim: build/slim
	docker push ghcr.io/elnoro/clip-embeddings-api:v0-slim

build/preloaded:
	docker build . --build-arg RUN_LOAD_MODEL=true -t ghcr.io/elnoro/clip-embeddings-api:v0-preloaded

test:
	PYTHONPATH="${PYTHONPATH}:/app" pytest

testC:
	docker compose exec app make test