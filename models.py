from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel



class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    accommodationType: bool
    currentCity: str
    currentState: str
    currentStreet: str
    currentZone: str
    desiredCity: str
    desiredState: str
    desiredStreet: str
    desiredZone: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    accommodationType = Column(Boolean, default=False)
    currentCity=Column(String)
    currentState=Column(String)
    currentStreet=Column(String)
    currentZone=Column(String)
    desiredCity=Column(String)
    desiredState=Column(String)
    desiredStreet=Column(String)
    desiredZone=Column(String)

class Houses(Base):
    __tablename__ = 'houses'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    address = Column(String)
    square = Column(String)
    city = Column(String)
    square_m = Column(Integer)
    rent = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))
    square_id = Column(Integer, ForeignKey('squares.id'))
    city_id = Column(Integer, ForeignKey('cities.id'))
    air_conditioner = Column(Boolean, default=False)
    smoking_allowed = Column(Boolean, default=False)
    pets = Column(Boolean, default=False)
    heating = Column(Boolean, default=False)

class Squares(Base):
    __tablename__ = 'squares'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    city = Column(String)
    province = Column(String)
    average_rent = Column(Integer)
    offers_num = Column(Integer)

class Cities(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    province = Column(String)
    offers_num = Column(Integer)
