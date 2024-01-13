## CLIP embeddings API

A single endpoint that accepts urls to jpg and returns embeddings

Uses fastapi, HF sequence transformers and nginx unit.

Build:

```
$ docker build . -t clipembeddingsapi
```
Run:
```
$ docker run --name clip-api --rm -p 8000:8000 -it clipembeddingsapi
```