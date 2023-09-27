from fastapi import APIRouter
from database import SessionLocal

def create_router(prefix: str, tags: list):
    return APIRouter(
        prefix= '/api'+ prefix,
        tags=tags
    )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
