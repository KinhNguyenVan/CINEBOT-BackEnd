from sqlalchemy.orm import Session
from sqlalchemy import func, desc, extract
from datetime import datetime, timedelta
from datetime import date
from app.models.movie import Movie
from app.models.showtime import Showtime
from app.models.ticket import Ticket
from app.models.room import Room
from sqlalchemy import and_

# Truy xuất phim đang chiếu (tồn tại trong lịch chiếu từ hôm nay trở đi)
def get_now_showing_movies(db: Session):
    now = datetime.now()
    next_24h = now + timedelta(hours=48)

    # Lấy tất cả suất chiếu trong 24 giờ tới
    showtimes = (
        db.query(Showtime)
        .filter(
            and_(
                (Showtime.date > now.date()) |
                ((Showtime.date == now.date()) & (Showtime.time >= now.time())),
                (Showtime.date < next_24h.date()) |
                ((Showtime.date == next_24h.date()) & (Showtime.time <= next_24h.time()))
            )
        )
        .all()
    )

    movie_map = {}

    for show in showtimes:
        movie = db.query(Movie).filter(Movie.id == show.movie_id).first()
        room = db.query(Room).filter(Room.id == show.room_id).first()

        if not movie:
            continue

        show_datetime = datetime.combine(show.date, show.time)
        show_info = {
            "time": show_datetime.strftime("%H:%M"),
            "date": show_datetime.strftime("%d/%m/%Y"),
            "room": room.name if room else "Phòng chưa rõ",
            "price": "100.000đ"
        }

        if movie.id not in movie_map:
            movie_map[movie.id] = {
                "id": movie.id,
                "title": movie.name,
                "genre": movie.genre,
                "showtimes": [show_info],
                "ageRating":movie.actors,
                "image": movie.poster
            }
        else:
            movie_map[movie.id]["showtimes"].append(show_info)
    
    return movie_map


def get_top_watched_movies(db: Session, limit: int = 5, days: int = 7):
    seven_days_ago = datetime.now().date() - timedelta(days=days)

    # Join Ticket -> Showtime -> Movie
    results = (
        db.query(Movie, func.count(Ticket.id).label("views"))
        .join(Showtime, Showtime.id == Ticket.showtime_id)
        .join(Movie, Movie.id == Showtime.movie_id)
        .filter(Ticket.booking_date >= seven_days_ago)
        .group_by(Movie.id)
        .order_by(func.count(Ticket.id).desc())
        .limit(limit)
        .all()
    )

    top_movies = [
        {
            "id": movie.id,
            "title": movie.name,
            "genre": movie.genre,
            "ageRating": movie.actors,  
            "viewCount": views,
            "image": movie.poster
        }
        for movie, views in results
    ]
    return top_movies



def get_movies_by_date(day: date, db: Session):
    results = (
        db.query(Movie)
        .join(Showtime, Movie.id == Showtime.movie_id)
        .filter(Showtime.date == day)
        .distinct(Movie.id)  # tránh bị trùng phim nếu có nhiều suất chiếu
        .all()
    )

    return [
        {
            "id": movie.id,
            "title": movie.name,
            "genre": movie.genre,
            "producer": movie.nsx,
            "actors": movie.actors
        }
        for movie in results
    ]

