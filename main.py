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

# Модель запроса
class BannerRequest(BaseModel):
    prompt: str
    style: str
    width: int
    height: int

# Новый API-ключ
RECRAFT_API_KEY = "vcZRwMLmLlJtxB6GPeiMatFoXfNHMQL1JwJkDbZiMABMT0cmvknQZd2F88cxJXmW"
RECRAFT_API_URL = "https://external.api.recraft.ai/v1/images/generations"

@app.post("/generate-banner")
def generate_banner(request: BannerRequest):
    try:
        # Параметры запроса согласно документации Recraft API
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
        
        # Отправка запроса
        response = requests.post(RECRAFT_API_URL, json=payload, headers=headers)
        response.raise_for_status()

        # Проверка результата
        data = response.json()
        image_url = data.get("image", None)  # Верное поле для URL изображения

        if image_url:
            return {"success": True, "data": {"image_url": image_url}}
        else:
            return {"success": False, "message": "Failed to fetch image URL"}

    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}

@app.get("/")
def root():
    return {"message": "FastAPI backend is running!"}
