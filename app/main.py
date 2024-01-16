import secrets
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from PIL import Image
from pydantic import BaseModel
import base64
import os
from sentence_transformers import SentenceTransformer
import requests
from io import BytesIO
from fastapi import status

app = FastAPI()
model = SentenceTransformer(os.getenv("MODEL_NAME"))

security = HTTPBearer(auto_error=False)

def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    token = os.getenv("API_TOKEN")
    if token is None or token == "":
        return
    if credentials is None or credentials.credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    is_token_correct = secrets.compare_digest(credentials.credentials, token)
    if not is_token_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return credentials.credentials


@app.post("/encode/")
async def encode_image(url: str, username: str = Depends(get_current_user)):
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
async def encode_image_base64(image_data: ImageData, username: str = Depends(get_current_user)):
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
async def encode_query(query: QueryData, username: str = Depends(get_current_user)):
    try:
        query_emb = model.encode(query.query)
        return {"embedding": query_emb.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {e}")
