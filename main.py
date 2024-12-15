import requests
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class BannerRequest(BaseModel):
    text: str
    style: str
    width: int
    height: int

RECRAFT_API_KEY = "vcZRwMLmLlJtxB6GPeiMatFoXfNHMQL1JwJkDbZiMABMT0cmvknQZd2F88cxJXmW"
RECRAFT_API_URL = "https://external.api.recraft.ai/v1/images/generations"

@app.post("/generate-banner")
def generate_banner(request: BannerRequest):
    try:
        # Подготовка запроса
        payload = {
            "prompt": request.text,
            "style": request.style,
            "width": request.width,
            "height": request.height
        }
        headers = {
            "Authorization": f"Bearer {RECRAFT_API_KEY}",
            "Content-Type": "application/json"
        }
        # Запрос к Recraft API
        response = requests.post(RECRAFT_API_URL, json=payload, headers=headers)
        response.raise_for_status()

        # Получение URL изображения
        data = response.json()
        image_url = data.get("data", [{}])[0].get("url")  # Извлечение по пути data[0].url
        if not image_url:
            return {"success": False, "message": "Image URL not found in response"}

        return {"success": True, "data": {"image_url": image_url}}
    except requests.exceptions.RequestException as e:
        return {"success": False, "message": f"Request error: {str(e)}"}

@app.get("/")
def root():
    return {"message": "FastAPI backend is running"}
