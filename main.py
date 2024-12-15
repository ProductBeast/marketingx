from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

RECRAFT_API_KEY = "vcZRwMLmLlJtxB6GPeiMatFoXfNHMQL1JwJkDbZiMABMT0cmvknQZd2F88cxJXmW"
RECRAFT_API_URL = "https://external.api.recraft.ai/v1/images/generations"


@app.post("/generate-banner")
async def generate_banner(
    business_description: str = Form(...),
    headline: str = Form(...),
    style: str = Form("digital_illustration")
):
    try:
        # Формирование промпта на основе входных данных
        prompt = (
            f"Design a banner for a business: '{business_description}'. "
            f"Include the headline: '{headline}' in the design. "
            f"The style should be: '{style}'. "
            f"The design should look clean, professional, and visually appealing."
        )

        # Запрос к Recraft API
        payload = {
            "prompt": prompt,
            "style": style
        }
        headers = {"Authorization": f"Bearer {RECRAFT_API_KEY}"}

        response = requests.post(RECRAFT_API_URL, json=payload, headers=headers)
        response.raise_for_status()

        # Получение URL изображения из ответа
        image_url = response.json()["data"][0]["url"]
        return {"success": True, "data": {"image_url": image_url}}

    except Exception as e:
        return {"success": False, "message": str(e)}


@app.get("/")
def root():
    return {"message": "FastAPI backend is running"}
