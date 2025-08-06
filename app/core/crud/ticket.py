from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from app.models.user import User
from app.models.showtime import Showtime
from app.models.movie import Movie
from app.models.seat import Seat
from app.models.room import Room
import json
from app.schemas.ticket import TicketCreate, TicketUserInput,GetTicketInput
from datetime import date
from app.core.crud.showtime import get_showtime_id_by_info
from app.core.crud.seat import get_seat_ids_by_names



def create_ticket(db: Session, ticket_data: TicketCreate):
    ticket = Ticket(**ticket_data.model_dump())
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket




def create_ticket_from_user_info(
    db: Session,
    user_input: TicketUserInput
):
    showtime_id = get_showtime_id_by_info(db, user_input.movie_name, user_input.date_, user_input.time_)
    if not showtime_id:
        return f"Không tìm thấy lịch chiếu vào ngày {user_input.date_} - {user_input.time_}"

    try:
        seats = get_seat_ids_by_names(db, user_input.seat_name)
    except ValueError as e:
        return str(e)

    showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    movie = db.query(Movie).filter(Movie.id == showtime.movie_id).first()
    room = db.query(Room).filter(Room.id == showtime.room_id).first()

    ticket_infos = []

    for seat in seats:
        ticket_data = TicketCreate(
            booking_date=date.today(),
            email=user_input.email,
            showtime_id=showtime_id,
            seat_id=seat.id
        )
        ticket = create_ticket(db, ticket_data)

        ticket_infos.append({
            "ticket_id": ticket.id,
            "booking_date": ticket.booking_date.strftime("%Y-%m-%d"),
            "movie_name": movie.name,
            "date": showtime.date.strftime("%Y-%m-%d"),
            "time": showtime.time.strftime("%H:%M"),
            "seat_name": seat.name,
            "room_name": room.name,
        })
    return ticket_infos

    

def get_ticket_by_email(db: Session, input: GetTicketInput):


    # Trích xuất email string từ input
    if isinstance(input, str):
        email_str = input
    elif isinstance(input, GetTicketInput):
        email_str = input.email
    else:
        return "Định dạng email không hợp lệ."
    tickets = (
        db.query(Ticket)
        .filter(Ticket.email == email_str)
        .join(Showtime, Ticket.showtime_id == Showtime.id)
        .join(Movie, Showtime.movie_id == Movie.id)
        .join(Room, Showtime.room_id == Room.id)
        .join(Seat, Ticket.seat_id == Seat.id)
        .order_by(Ticket.booking_date.desc())
        .all()
    )

    if not tickets:
        return []

    result = []
    for ticket in tickets:
        result.append({
            "ticket_id": ticket.id,
            "booking_date": ticket.booking_date.strftime("%Y-%m-%d"),
            "movie_name": ticket.showtime.movie.name,
            "date": ticket.showtime.date.strftime("%Y-%m-%d"),
            "time": ticket.showtime.time.strftime("%H:%M"),
            "room_name": ticket.showtime.room.name,
            "seat_name": ticket.seat.name,
            "price": "100.000đ"
        })

    return result




