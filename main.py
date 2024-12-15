from fastapi import FastAPI
from pydantic import BaseModel

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
