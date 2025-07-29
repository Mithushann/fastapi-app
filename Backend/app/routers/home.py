# app/routers/example.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    return {"message": "This is the root endpoint of the FastAPI application. The API is running successfully!"}
