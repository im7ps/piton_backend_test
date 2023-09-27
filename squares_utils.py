"""
from models import Houses, Squares, Cities
from database import SessionLocal


def square_average_rent(db: SessionLocal, square_name: str):
    # Trova il quartiere corrispondente al nome specificato
    square = db.query(Squares).filter(Squares.title == square_name).first()

    if not square:
        raise ValueError("Il quartiere specificato non esiste.")

    # Trova tutte le case nel quartiere specificato
    houses_in_square = db.query(Houses).filter(Houses.square_id == square.id).all()

    if not houses_in_square:
        return 0  # Se non ci sono case nel quartiere, l'affitto medio sarà 0

    # Calcola l'affitto medio delle case nel quartiere
    total_rent = sum(house.average_rent for house in houses_in_square)
    average_rent = total_rent / len(houses_in_square)

    return average_rent

    """
from sqlalchemy import func
from models import Houses, Squares
from database import SessionLocal

def square_average_rent(db: SessionLocal, square_name: str):
    # Trova il quartiere corrispondente al nome specificato
    square = db.query(Squares).filter(Squares.title == square_name).first()

    if not square:
        raise ValueError("Il quartiere specificato non esiste.")

    # Calcola l'affitto medio delle case nel quartiere
    average_rent = (
        db.query(func.avg(Houses.rent))
        .filter(Houses.square == square.title) #IMPORTANTE: usando title al posto di id worka, quindi gli id sono sconnessi
        .scalar() or 0  # Restituisci 0 se non ci sono case nel quartiere
    )

    return average_rent
