from sqlalchemy.orm import Session
from app.core.crud import movie
from datetime import date

def get_now_showing(db: Session):
    return movie.get_now_showing_movies(db)

def get_top_movies(db: Session, limit: int = 5, days: int = 7):
    return movie.get_top_watched_movies(db, limit, days)

def get_movies_by_date(db:Session,day:date):
    return movie.get_movies_by_date(day=day,db = db)