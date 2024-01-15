import httpx
import pytest
import base64
from PIL import Image
from io import BytesIO
from app.main import app

@pytest.fixture
def test_client():
    return httpx.AsyncClient(app=app, base_url="http://test")

@pytest.mark.asyncio
async def test_encode_image_base64(test_client):
    dummy_img = Image.new('RGB', (100, 100))
    buf = BytesIO()
    dummy_img.save(buf, format='JPEG')
    img_bytes = buf.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')

    response = await test_client.post("/encode-base64/", json={"file": img_base64})
    
    assert response.status_code == 200
    assert "embedding" in response.json()
    assert len(response.json()["embedding"]) == 512