from typing import Annotated
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Houses
from database import SessionLocal
from .auth import get_current_user
from services import get_db, create_router

router = create_router(prefix='/features', tags=['features'])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class HouseFeaturesRequest(BaseModel):
    air_conditioner: bool = False
    smoking_allowed: bool = False
    pets: bool = False
    heating: bool = False


@router.put("/houses/{house_id}/features", status_code=status.HTTP_202_ACCEPTED)
async def update_feature(db: db_dependency, house_request: HouseFeaturesRequest, house_id: int = Path(gt=0)):
    house = db.query(Houses).filter(Houses.id == house_id).first()
    if house is None:
        raise HTTPException(status_code=404, detail="House not found.")
    house.air_conditioner = house_request.air_conditioner
    house.smoking_allowed = house_request.smoking_allowed
    house.pets = house_request.pets
    house.heating = house_request.heating
    db.add(house)
    db.commit()
