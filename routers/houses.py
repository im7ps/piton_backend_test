from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Houses, Squares, Cities
from database import SessionLocal
from .auth import get_current_user
import houses_utils
from services import get_db, create_router

router = create_router(prefix='/houses', tags=['houses'])


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class HouseRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    address: str = Field(min_length=3, max_length=100)
    square: str = Field(min_length=3, max_length=32)
    city: str = Field(min_length=3, max_length=32)
    square_m: int = Field(gt=0)
    rent: int = Field(gt=0)
    air_conditioner: bool = Field(default=False)
    smoking_allowed: bool = Field(default=False)
    pets: bool = Field(default=False)
    heating: bool = Field(default=False)


@router.get("/")
async def get_houses(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")
    return db.query(Houses).all()


@router.get("/houses/{house_id}", status_code=status.HTTP_200_OK)
async def get_house_by_id(user: user_dependency, db: db_dependency, house_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")
    house = db.query(Houses).filter(Houses.id == house_id).filter(Houses.owner_id == user.get('id')).first()
    if house is not None:
        return house
    raise HTTPException(status_code=404, detail="House not found.")


@router.post("/house", status_code=status.HTTP_201_CREATED)
async def create_house(user: user_dependency, db: db_dependency, house_request: HouseRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")
    #Ottenere gli oggetti Square e City in base ai nomi forniti
    square_obj = db.query(Squares).filter_by(title=house_request.square).first()
    city_obj = db.query(Cities).filter_by(title=house_request.city).first()

    house = Houses (
        **house_request.dict(),
        owner_id=user.get('id'),
        square_id=square_obj.id if square_obj else None,
        city_id=city_obj.id if city_obj else None
    )
    db.add(house)
    db.commit()
    houses_utils.update_offers_num(db, house_request.square, house_request.city)
    

@router.put("/houses/{house_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_house(user: user_dependency, db: db_dependency, house_request: HouseRequest, house_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")
    house = db.query(Houses).filter(Houses.id == house_id).filter(Houses.owner_id == user.get('id')).first()
    if house is None:
        raise HTTPException(status_code=404, detail="House not found.")
    house.title = house_request.title
    house.description = house_request.description
    house.address = house_request.address
    house.square = house_request.square
    house.city = house_request.city
    house.square_m = house_request.square_m
    house.rent = house_request.rent
    house.air_conditioner = house_request.air_conditioner
    house.smoking_allowed = house_request.smoking_allowed
    house.pets = house_request.pets
    house.heating = house_request.heating
    db.add(house)
    db.commit()


@router.delete("houses/{house_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_house(user: user_dependency, db: db_dependency, house_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")
    house = db.query(Houses).filter(Houses.id == house_id).filter(Houses.owner_id == user.get('id')).first()
    if house is None:
        raise HTTPException(status_code=404, detail="House not found.")
    db.query(Houses).filter(Houses.id == house_id).filter(Houses.owner_id == user.get('id')).delete()
    db.commit()