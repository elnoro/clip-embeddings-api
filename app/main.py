from fastapi import FastAPI, HTTPException
from PIL import Image
from pydantic import BaseModel
import base64
import os
from sentence_transformers import SentenceTransformer
import requests
from io import BytesIO

app = FastAPI()
model = SentenceTransformer(os.getenv("MODEL_NAME"))


@app.post("/encode/")
async def encode_image(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        img_emb = model.encode(img)
        return {"embedding": img_emb.tolist()}
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error fetching image: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {e}")


class ImageData(BaseModel):
    file: str


@app.post("/encode-base64/")
async def encode_image_base64(image_data: ImageData):
    try:
        image_data = BytesIO(base64.b64decode(image_data.file))
        img = Image.open(image_data)
        img_emb = model.encode(img)
        return {"embedding": img_emb.tolist()}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error decoding and processing image: {e}"
        )


class QueryData(BaseModel):
    query: str


@app.post("/encode-query/")
async def encode_query(query: QueryData):
    try:
        query_emb = model.encode(query.query)
        return {"embedding": query_emb.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {e}")
