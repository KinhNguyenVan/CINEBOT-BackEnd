from app.models.seat import Seat
from sqlalchemy.orm import Session
from app.models.showtime import Showtime
from app.models.status_seat import SeatStatus
from app.models.movie import Movie
from app.models.ticket import Ticket
import json
from datetime import date, time
from typing import List
from sqlalchemy import asc,func,desc
from app.utils.normalize_string import normalize_string


def get_seat_ids_by_names(db: Session, seat_names: List[str]) -> List[Seat]:
    seats = db.query(Seat).filter(Seat.name.in_(seat_names)).all()

    if len(seats) != len(seat_names):
        found = {s.name for s in seats}
        missing = set(seat_names) - found
        raise ValueError(f"Không tìm thấy các ghế: {', '.join(missing)}")

    return seats  



def get_available_seats(db: Session, movie_name: str, show_date: date, show_time: time):
    # Tìm suất chiếu theo tên phim, ngày, giờ
    SIMILARITY_THRESHOLD = 0.12
    normalized_input = normalize_string(movie_name)

    # Tìm showtime khớp ngày + giờ + tên phim gần đúng nhất
    showtime = (
        db.query(Showtime)
        .join(Movie, Showtime.movie_id == Movie.id)
        .filter(
            Showtime.date == show_date,
            Showtime.time == show_time,
            func.similarity(func.unaccent(Movie.name), normalized_input) > SIMILARITY_THRESHOLD
        )
        .order_by(desc(func.similarity(func.unaccent(Movie.name), normalized_input)))
        .first()
    )

    if not showtime:
        return f"Không tìm thấy suất chiếu phù hợp cho phim '{movie_name}' vào {show_date} {show_time}."

    room_id = showtime.room_id
    showtime_id = showtime.id

    # Lấy tất cả ghế trong phòng (kèm tên ghế)
    all_seats = (
        db.query(Seat.id, Seat.name)
        .join(SeatStatus, Seat.id == SeatStatus.seat_id)
        .filter(SeatStatus.room_id == room_id)
        .all()
    )

    if not all_seats:
        return "Không có ghế nào trong phòng chiếu."

    all_seat_map = {seat.id: seat.name for seat in all_seats}

    # Lấy danh sách ghế đã đặt trong suất chiếu này
    booked_seat_ids = (
        db.query(Ticket.seat_id)
        .filter(Ticket.showtime_id == showtime_id)
        .all()
    )
    booked_seat_ids = {seat_id for (seat_id,) in booked_seat_ids}
    # Ghế còn trống = tất cả ghế - ghế đã đặt
    available_seats = [
        seat_name
        for seat_id, seat_name in all_seat_map.items()
        if seat_id not in booked_seat_ids
    ]

    if not available_seats:
        return "Tất cả ghế trong phòng đã được đặt."

    return json.dumps({
        "movie_name": movie_name,
        "date": show_date.strftime("%Y-%m-%d"),
        "time": show_time.strftime("%H:%M"),
        "available_seat_names": sorted(available_seats)
    }, ensure_ascii=False, indent=2)