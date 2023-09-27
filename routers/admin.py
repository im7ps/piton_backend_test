from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Houses
from database import SessionLocal
from .auth import get_current_user
from services import get_db, create_router

router = create_router(prefix='/admin', tags=['admin'])


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/house", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Need to be Admin!')
    return db.query(Houses).all()


@router.delete("/house/{house_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_house(user: user_dependency, db: db_dependency, house_id: int = Path(gt=0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Need to be Admin!')
    house_model = db.query(Houses).filter(Houses.id == house_id).first()
    if house_model is None:
        raise HTTPException(status_code=404, detail='house not found.')
    db.query(Houses).filter(Houses.id == house_id).delete()
    db.commit()
