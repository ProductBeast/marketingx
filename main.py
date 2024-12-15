import requests
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai

app = FastAPI()

# Middleware для CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ключи API
RECRAFT_API_KEY = "vcZRwMLmLlJtxB6GPeiMatFoXfNHMQL1JwJkDbZiMABMT0cmvknQZd2F88cxJXmW"
OPENAI_API_KEY = "ваш_openai_api_ключ"

# Инициализация OpenAI
openai.api_key = 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

RECRAFT_API_URL = "https://external.api.recraft.ai/v1/images/generations"

# Модель запроса
class BannerRequest(BaseModel):
    business_description: str
    banner_headline: str
    style: str = "digital_illustration"  # Стиль по умолчанию


@app.post("/generate-banner")
def generate_banner(request: BannerRequest):
    try:
        # Генерация мегапромпта с помощью OpenAI
        prompt = f"""
        Create a detailed banner design description based on the following details:
        Business Description: {request.business_description}
        Banner Headline: {request.banner_headline}
        Style: {request.style}

        Include elements like color palette, typography, layout, and any visual suggestions.
        Make the description clear, concise, and ready for image generation.
        """

        openai_response = openai.ChatCompletion.create(
            model="gpt-4",  # Используем gpt-4 или gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "You are an assistant specialized in creating detailed design prompts for banners."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )

        # Получаем мегапромпт
        generated_prompt = openai_response['choices'][0]['message']['content'].strip()

        # Отправляем запрос в Recraft API
        payload = {
            "prompt": generated_prompt,
            "style": request.style,
        }
        headers = {"Authorization": f"Bearer {RECRAFT_API_KEY}"}

        recraft_response = requests.post(RECRAFT_API_URL, json=payload, headers=headers)
        recraft_response.raise_for_status()

        # Получаем URL изображения
        image_url = recraft_response.json()["data"][0]["url"]

        return {"success": True, "image_url": image_url}

    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/")
def root():
    return {"message": "API is running"}
