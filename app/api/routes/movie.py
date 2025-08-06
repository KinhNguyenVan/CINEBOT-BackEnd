from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.service import movie_service
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/movies/now_showing")
def now_showing(db: Session = Depends(get_db)):
    movies = movie_service.get_now_showing(db)
    return JSONResponse(content=list(movies.values()))

@router.get("/movies/top_watched")
def top_movies(limit: int = 5, days: int = 7, db: Session = Depends(get_db)):
    moives = movie_service.get_top_movies(db, limit, days)
    return JSONResponse(content=moives)

