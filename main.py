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

# Ваш ключ Recraft API
RECRAFT_API_KEY = "nbMF57gbMPui8ItRZdfIGqM9asqhp4lJ2hHOpXngOQuAWsjzjvRqs5Ps9cK68Lzy"
RECRAFT_API_URL = "https://api.recraft.ai/v3/generate"

@app.post("/generate-banner")
def generate_banner(request: BannerRequest):
    try:
        # Подготовка запроса к Recraft API
        payload = {
            "text": request.text,
            "style": request.style,
            "width": request.width,
            "height": request.height
        }
        headers = {"Authorization": f"Bearer {RECRAFT_API_KEY}"}

        # Отправка запроса
        response = requests.post(RECRAFT_API_URL, json=payload, headers=headers)
        response.raise_for_status()

        # Логирование ответа
        print("Recraft API Response:", response.json())

        # Получение URL изображения
        image_url = response.json().get("image_url")
        if not image_url:
            return {"success": False, "message": "Image URL not found in Recraft API response"}

        # Возвращаем ссылку на изображение
        return {"success": True, "data": {"image_url": image_url}}
    except Exception as e:
        return {"success": False, "message": str(e)}

@app.get("/")
def root():
    return {"message": "FastAPI backend is running"}
