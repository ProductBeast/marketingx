import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS Middleware для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic модель для данных запроса
class GenerateImageRequest(BaseModel):
    prompt: str
    style: str

# Recraft API ключ и URL
RECRAFT_API_KEY = "vcZRwMLmLlJtxB6GPeiMatFoXfNHMQL1JwJkDbZiMABMT0cmvknQZd2F88cxJXmW"
RECRAFT_API_URL = "https://external.api.recraft.ai/v1/images/generations"

@app.post("/generate-banner")
def generate_banner(request: GenerateImageRequest):
    try:
        # Формирование запроса к Recraft API
        payload = {
            "prompt": request.prompt,
            "style": request.style
        }
        headers = {
            "Authorization": f"Bearer {RECRAFT_API_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.post(RECRAFT_API_URL, json=payload, headers=headers)
        response.raise_for_status()

        # Получаем URL изображения из ответа
        data = response.json()
        image_url = data["data"][0]["url"]

        return {"success": True, "data": {"image_url": image_url}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

@app.get("/")
def root():
    return {"message": "FastAPI backend for Recraft Image Generator is running!"}
