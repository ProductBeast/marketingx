from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data model for request
class BannerRequest(BaseModel):
    business_description: str
    banner_headline: str
    style: str

RECRAFT_API_KEY = "vcZRwMLmLlJtxB6GPeiMatFoXfNHMQL1JwJkDbZiMABMT0cmvknQZd2F88cxJXmW"
RECRAFT_API_URL = "https://external.api.recraft.ai/v1/images/generations"

@app.post("/generate-banner")
def generate_banner(request: BannerRequest):
    # Combine inputs into a single prompt
    combined_prompt = (
        f"Design a banner for {request.business_description}. "
        f"Include the headline '{request.banner_headline}'. "
        f"Make the style match {request.style}."
    )

    payload = {
        "prompt": combined_prompt,
        "style": request.style
    }
    headers = {"Authorization": f"Bearer {RECRAFT_API_KEY}"}

    # Send the request to Recraft API
    try:
        response = requests.post(RECRAFT_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        image_url = response.json().get("data")[0].get("url")
        return {"success": True, "image_url": image_url}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/")
def read_root():
    return {"message": "Banner Generator API is running!"}
