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
    return {"success": True, "message": "Banner generated successfully", "data": request.dict()}

@app.get("/")
def read_root():
    return {"message": "FastAPI backend is running!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить запросы с любого домена. Для безопасности позже можно указать точные домены.
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить любые HTTP методы (POST, GET и т.д.)
    allow_headers=["*"],  # Разрешить любые заголовки
)
