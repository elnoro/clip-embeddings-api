from fastapi import FastAPI, HTTPException
from PIL import Image
from pydantic import BaseModel
import base64
from sentence_transformers import SentenceTransformer
import requests
from io import BytesIO

app = FastAPI()
model = SentenceTransformer('clip-ViT-B-32')

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
        raise HTTPException(status_code=500, detail=f"Error decoding and processing image: {e}")
