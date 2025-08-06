from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.service.showtime_service import get_showtimes_by_movie_and_date

router = APIRouter()

@router.get("/movies/{movie_name}/showtimes")
def read_showtimes(movie_name: str, db: Session = Depends(get_db)):
    return get_showtimes_by_movie_and_date(db, movie_name)
