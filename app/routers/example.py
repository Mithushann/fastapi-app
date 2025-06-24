# app/routers/example.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/example")
def root():
    return {"message": "CI/CD FastAPI Docker Setup"}
