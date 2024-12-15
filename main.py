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

RECRAFT_API_KEY = "ваш_ключ_Recraft"
RECRAFT_API_URL = "https://api.recraft.ai/v3/generate"

@app.post("/generate-banner")
def generate_banner(request: BannerRequest):
    # Отправка запроса к Recraft API
    try:
        payload = {
            "text": request.text,
            "style": request.style,
            "width": request.width,
            "height": request.height
        }
        headers = {"Authorization": f"Bearer {RECRAFT_API_KEY}"}
        response = requests.post(RECRAFT_API_URL, json=payload, headers=headers)
        response.raise_for_status()  # Проверка на ошибки

        # Получение URL изображения из ответа
        image_url = response.json().get("image_url")
        if not image_url:
            return {"success": False, "message": "Failed to generate image from Recraft API"}

        return {"success": True, "data": {"image_url": image_url}}
    except Exception as e:
        return {"success": False, "message": str(e)}

@app.get("/")
def root():
    return {"message": "FastAPI backend is running"}
