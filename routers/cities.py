from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Cities
from database import SessionLocal
from .auth import get_current_user
from pydantic import BaseModel, Field
from services import get_db, create_router

router = create_router(prefix='/cities', tags=['cities'])


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class CityRequest(BaseModel):
    title: str = Field(min_length=3, max_length=32)
    province: str = Field(min_length=2, max_length=2)


@router.get("/")
async def get_cities(db: db_dependency):
    return db.query(Cities).all()


@router.get("/cities/{city_id}", status_code=status.HTTP_200_OK)
async def get_city_by_id(db: db_dependency, city_id: int = Path(gt=0)):
    city = db.query(Cities).filter(Cities.id == city_id).first()
    if city is not None:
        return city
    raise HTTPException(status_code=404, detail="House not found.")


@router.get("/cities/{city_title}", status_code=status.HTTP_200_OK)
async def get_city_by_id(db: db_dependency, city_title: str = Path(min_length=3)):
    city = db.query(Cities).filter(Cities.title == city_title).first()
    if city is not None:
        return city
    raise HTTPException(status_code=404, detail="House not found.")


@router.post("/city", status_code=status.HTTP_201_CREATED)
async def create_city(user: user_dependency, db: db_dependency, city_request: CityRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")
    city = Cities(**city_request.dict())
    db.add(city)
    db.commit()