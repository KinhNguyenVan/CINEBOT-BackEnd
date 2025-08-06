from sqlalchemy.orm import Session
from sqlalchemy import asc,func,desc
from app.models.movie import Movie
from app.models.showtime import Showtime
from app.models.room import Room
from app.utils.normalize_string import normalize_string
from datetime import datetime,date,time, timedelta
import json

def get_showtimes_by_movie_and_date(db: Session, movie_name: str,day:date):
    current_time = datetime.now()
    SIMILARITY_THRESHOLD = 0.2
    normalized_input = normalize_string(movie_name)
    similarity_score = func.similarity(func.unaccent(Movie.name), normalized_input)
    movies = (
        db.query(Movie)
        .filter(similarity_score > SIMILARITY_THRESHOLD)
        .order_by(desc(similarity_score))
        .limit(5)
        .all() 
    )

    if not movies:
        return  f"Không có lịch chiếu phim {movie_name} vào ngày {day}."
    result = []
    for movie in movies:
        
        # Lấy tất cả lịch chiếu sắp xếp theo ngày rồi đến giờ
        showtimes = (
            db.query(Showtime)
            .filter(Showtime.movie_id == movie.id,Showtime.date == day)
            .join(Room, Showtime.room_id == Room.id)
            .order_by(asc(Showtime.date), asc(Showtime.time))
            .all()
        )
        for st in showtimes:
            show_datetime = datetime.combine(st.date, st.time)
            

            if show_datetime >= current_time:  # chỉ lấy lịch chiếu trong tương lai
                result.append({
                    "showtime_id": st.id,
                    "date": st.date.strftime("%Y-%m-%d"),
                    "time": st.time.strftime("%H:%M"),
                    "room_name": st.room.name,
                    "movie_name": movie.name
                })

    if not result:
        return "Không có lịch chiếu phù hợp trong tương lai."

    return json.dumps(result, ensure_ascii=False, indent=2)


def get_showtime_id_by_info(
    db: Session, movie_name: str, date_: date, time_: time) -> str:
    SIMILARITY_THRESHOLD = 0.12
    normalized_input = normalize_string(movie_name)  # Bỏ dấu, chuẩn hóa tên

    movie = (
        db.query(Movie)
        .filter(func.similarity(func.unaccent(Movie.name), normalized_input) > SIMILARITY_THRESHOLD)
        .order_by(desc(func.similarity(func.unaccent(Movie.name), normalized_input)))
        .first()
    )

    if not movie:
        return f"Không tìm thấy phim tên {movie_name}"

    showtime = (
        db.query(Showtime)
        .filter(
            Showtime.movie_id == movie.id,
            Showtime.date == date_,
            Showtime.time == time_,
        )
        .first()
    )

    if not showtime:
        return f"Không tìm thấy suất chiếu cho phim {movie_name}"

    return showtime.id


def get_showtimes_by_date(db: Session, day: date):
    current_time = datetime.now()

    # Lấy tất cả lịch chiếu theo ngày đã cho
    showtimes = (
        db.query(Showtime)
        .filter(Showtime.date == day)
        .join(Movie, Showtime.movie_id == Movie.id)
        .join(Room, Showtime.room_id == Room.id)
        .order_by(asc(Showtime.time))
        .all()
    )

    if not showtimes:
        return f"Không có lịch chiếu nào vào ngày {day.strftime('%Y-%m-%d')}."

    result = []
    for st in showtimes:

        # Chỉ lọc các lịch chiếu trong tương lai nếu ngày là hôm nay
        if st.date > current_time.date() or (st.date == current_time.date() and st.time >= current_time.time()):
            result.append({
                "showtime_id": st.id,
                "movie_name": st.movie.name,
                "room_name": st.room.name,
                "date": st.date.strftime("%Y-%m-%d"),
                "time": st.time.strftime("%H:%M")
            })

    if not result:
        return f"Không có lịch chiếu nào còn lại trong ngày {day.strftime('%Y-%m-%d')}."

    return json.dumps(result, ensure_ascii=False, indent=2)

def get_showtimes_by_movie(db: Session, movie_name: str, range_day: int = 5):
    current_time = datetime.now()
    today = current_time.date()
    end_date = today + timedelta(days=range_day)
    SIMILARITY_THRESHOLD = 0.12
    normalized_input = normalize_string(movie_name)
    similarity_score = func.similarity(func.unaccent(Movie.name), normalized_input)
    movies = (
        db.query(Movie)
        .filter(similarity_score > SIMILARITY_THRESHOLD)
        .order_by(desc(similarity_score))
        .limit(5)
        .all() 
    )


    if not movies:
        return f"Không tìm thấy phim nào với tên gần giống '{movie_name}'."

    result = []

    for movie in movies:
        showtimes = (
            db.query(Showtime)
            .filter(
                Showtime.movie_id == movie.id,
                Showtime.date >= today,
                Showtime.date <= end_date
            )
            .join(Room, Showtime.room_id == Room.id)
            .order_by(Showtime.date.asc(), Showtime.time.asc())
            .all()
        )

        for st in showtimes:
            show_datetime = datetime.combine(st.date, st.time)

            if show_datetime >= current_time:
                result.append({
                    "showtime_id": st.id,
                    "movie_name": movie.name,
                    "date": st.date.strftime("%Y-%m-%d"),
                    "time": st.time.strftime("%H:%M"),
                    "room_name": st.room.name
                })

    if not result:
        return f"Không có lịch chiếu sắp tới cho các phim gần giống '{movie_name}' trong {range_day} ngày tới."

    return json.dumps(result, ensure_ascii=False, indent=2)
