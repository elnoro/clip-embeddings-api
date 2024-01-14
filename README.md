## CLIP embeddings API

A single endpoint that accepts urls to jpg and returns embeddings

Build it yourself:
```
$ docker build . --build-arg RUN_LOAD_MODEL=true -t clipembeddingsapi
$ docker run --name clip-api --rm -p 8000:8000 clipembeddingsapi
```

Run image (model will be downloaded at runtime):
```
$ docker run --name clip-api --rm -p 8000:8000 ghcr.io/elnoro/clip-embeddings-api:v0-slim
```

Uses:

[Model](https://huggingface.co/sentence-transformers/clip-ViT-B-32)
[sentence-transformers](https://www.sbert.net/)
[FastAPI](https://fastapi.tiangolo.com/)