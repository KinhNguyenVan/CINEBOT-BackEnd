from sqlalchemy.orm import Session
from app.core.crud import seat
from datetime import date, time

def get_available_seats(db:Session,movie_name: str,show_date:date, show_time: time):
    return seat.get_available_seats(db,movie_name,show_date,show_time)
