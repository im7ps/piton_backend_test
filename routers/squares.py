from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Squares
from database import SessionLocal
from .auth import get_current_user
from pydantic import BaseModel, Field
import squares_utils
from services import get_db, create_router

router = create_router(prefix='/squares', tags=['squares'])


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class SquareRequest(BaseModel):
    title: str = Field(min_length=3)
    city: str = Field(min_length=3, max_length=32)
    province: str = Field(min_length=2, max_length=2)



@router.get("/")
async def get_squares(db: db_dependency):
    return db.query(Squares).all()


@router.get("/squares/{square_id}", status_code=status.HTTP_200_OK)
async def get_square_by_id(db: db_dependency, square_id: int = Path(gt=0)):
    square = db.query(Squares).filter(Squares.id == square_id).first()
    if square is not None:
        return square
    raise HTTPException(status_code=404, detail="Square not found.")


@router.get("/squares/{square_title}", status_code=status.HTTP_200_OK)
async def get_square_by_id(db: db_dependency, square_title: str = Path(min_length=3)):
    square = db.query(Squares).filter(Squares.title == square_title).first()
    if square is not None:
        return square
    raise HTTPException(status_code=404, detail="Square not found.")


@router.get("/squares/{square_id}/rent", status_code=status.HTTP_200_OK)
async def get_average_rent(db: db_dependency, square_id: int = Path(gt=0)):
    square = db.query(Squares).filter(Squares.id == square_id).first()
    if square is not None:
        return (squares_utils.square_average_rent(db, square.title))
    raise HTTPException(status_code=404, detail="Rent not found.")


@router.post("/square", status_code=status.HTTP_201_CREATED)
async def create_square(user: user_dependency, db: db_dependency, square_request: SquareRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")
    square = Squares(**square_request.dict())
    db.add(square)
    db.commit()
