from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import Users
from starlette import status


def verify_email(db: Session, email: str):
    existing_user = db.query(Users).filter(Users.email == email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
