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
        # Формирование запроса к Recraft API
        payload = {
            "prompt": request.text,  # Текст, используемый для генерации изображения
            "style": request.style,
            "width": request.width,
            "height": request.height
        }
        headers = {
            "Authorization": f"Bearer {RECRAFT_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(RECRAFT_API_URL, json=payload, headers=headers)
        response.raise_for_status()

        # Обработка ответа
        data = response.json()
        image_url = data.get("data", {}).get("image_url")

        if not image_url:
            return {"success": False, "message": "No image URL returned from API."}

        return {"success": True, "data": {"image_url": image_url}}

    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}

@app.get("/")
def root():
    return {"message": "FastAPI backend is running"}
