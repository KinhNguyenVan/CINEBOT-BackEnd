from sqlalchemy.orm import Session
from app.core.crud import showtime
from datetime import date

def get_showtimes_by_movie_and_date(db: Session, movie_name: str,day: date):
    return showtime.get_showtimes_by_movie_and_date(db, movie_name,day)

def get_showtimes_by_date(db:Session, day: date):
    return showtime.get_showtimes_by_date(db,day)

def get_showtimes_by_movie(db:Session,movie_name: str,range_day:int):
    return showtime.get_showtimes_by_movie(db,movie_name,range_day)