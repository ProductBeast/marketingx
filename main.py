import requests
from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модель запроса
class BannerRequest(BaseModel):
    prompt: str = Field(..., example="Generate a professional banner with text 'Hello'")
    style: str = Field("default", example="default")
    width: int = Field(512, ge=256, le=1024, example=512)  # ширина от 256 до 1024
    height: int = Field(512, ge=256, le=1024, example=512)  # высота от 256 до 1024

RECRAFT_API_KEY = "vcZRwMLmLlJtxB6GPeiMatFoXfNHMQL1JwJkDbZiMABMT0cmvknQZd2F88cxJXmW"
RECRAFT_API_URL = "https://external.api.recraft.ai/v1/images/generations"

@app.post("/generate-banner")
def generate_banner(request: BannerRequest):
    try:
        payload = {
            "prompt": request.prompt,
            "style": request.style,
            "width": request.width,
            "height": request.height
        }
        headers = {
            "Authorization": f"Bearer {RECRAFT_API_KEY}",
            "Content-Type": "application/json"
        }

        # Логирование данных запроса (для отладки)
        print("Sending payload:", payload)

        # Отправка запроса к Recraft API
        response = requests.post(RECRAFT_API_URL, json=payload, headers=headers)
        response.raise_for_status()  # Проверка на HTTP ошибки

        # Парсинг ответа
        data = response.json()
        image_url = data.get("image")

        if not image_url:
            return {"success": False, "message": "Image URL not found in response"}
        
        return {"success": True, "data": {"image_url": image_url}}

    except requests.exceptions.RequestException as e:
        return {"success": False, "message": f"Request error: {str(e)}"}

@app.get("/")
def root():
    return {"message": "FastAPI backend is running!"}
