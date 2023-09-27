"""
from models import Houses, Squares, Cities
from database import SessionLocal

def update_offers_num(db: SessionLocal, square: str, city: str):
    # Ottieni gli oggetti Square e City in base ai nomi forniti
    square_obj: Squares = db.query(Squares).filter_by(title=square).first()
    city_obj: Cities = db.query(Cities).filter_by(title=city).first()

    if square_obj and city_obj:
        # Calcola il numero di case per ogni square e city
        square_count = db.query(Houses).filter_by(square_id=square_obj.id).count()
        city_count = db.query(Houses).filter_by(city_id=city_obj.id).count()

        # Aggiorna i valori di offers_num per Square e City
        square_obj.offers_num = square_count
        city_obj.offers_num = city_count

        # Esegui il commit per rendere permanenti le modifiche al database
        db.commit()
    else:
        # Gli oggetti Square o City non sono stati trovati
        raise ValueError("Square or City not found")

"""
from sqlalchemy import func
from models import Houses, Squares, Cities
from database import SessionLocal

def update_offers_num(db: SessionLocal, square: str, city: str):
    # Ottieni gli oggetti Square e City in base ai nomi forniti
    square_obj: Squares = db.query(Squares).filter_by(title=square).first()
    city_obj: Cities = db.query(Cities).filter_by(title=city).first()

    if square_obj and city_obj:
        # Calcola il numero di case per ogni square e city
        square_counts = (
            db.query(Houses.square_id, func.count(Houses.id))
            .filter_by(square_id=square_obj.id)
            .group_by(Houses.square_id)
            .all()
        )
        
        city_counts = (
            db.query(Houses.city_id, func.count(Houses.id))
            .filter_by(city_id=city_obj.id)
            .group_by(Houses.city_id)
            .all()
        )

        # Aggiorna i valori di offers_num per Square e City
        square_obj.offers_num = sum(count for _, count in square_counts)
        city_obj.offers_num = sum(count for _, count in city_counts)

        # Esegui il commit per rendere permanenti le modifiche al database
        db.commit()
    else:
        # Gli oggetti Square o City non sono stati trovati
        raise ValueError("Square or City not found")
