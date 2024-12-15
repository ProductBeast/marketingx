from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class BannerRequest(BaseModel):
    text: str
    style: str
    width: int
    height: int

@app.post("/generate-banner")
def generate_banner(request: BannerRequest):
    # В реальном сценарии здесь будет логика генерации баннера
    # Пока возвращаем временный URL
    return {
        "success": True,
        "message": "Banner generated successfully",
        "data": {
            "image_url": "https://via.placeholder.com/{}x{}?text={}".format(
                request.width, request.height, request.text
            )
        },
    }

@app.get("/")
def read_root():
    return {"message": "FastAPI backend is running!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
