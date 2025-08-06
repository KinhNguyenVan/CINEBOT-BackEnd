from sqlalchemy.orm import relationship

from app.models.user import User
from app.models.account import Account
from app.models.ticket import Ticket
from app.models.seat import Seat
from app.models.room import Room
from app.models.movie import Movie
from app.models.showtime import Showtime

# --- Quan hệ 1-n giữa User và Account ---
User.account = relationship("Account", back_populates="user")
Account.user = relationship("User", back_populates="account")

# # --- Quan hệ 1-n giữa User và Ticket ---
# User.tickets = relationship("Ticket", back_populates="user")
# Ticket.user = relationship("User", back_populates="tickets")

# --- Quan hệ 1-n giữa Account và Ticket ---
Account.tickets = relationship("Ticket", back_populates="account")
Ticket.account = relationship("Account", back_populates="tickets")

# --- Quan hệ 1-n giữa Showtime và Ticket ---
Showtime.tickets = relationship("Ticket", back_populates="showtime")
Ticket.showtime = relationship("Showtime", back_populates="tickets")

# --- Quan hệ 1-n giữa Seat và Ticket ---
Seat.tickets = relationship("Ticket", back_populates="seat")
Ticket.seat = relationship("Seat", back_populates="tickets")

# --- Quan hệ 1-n giữa Movie và Showtime ---
Movie.showtimes = relationship("Showtime", back_populates="movie")
Showtime.movie = relationship("Movie", back_populates="showtimes")

# --- Quan hệ 1-n giữa Room và Showtime ---
Room.showtimes = relationship("Showtime", back_populates="room")
Showtime.room = relationship("Room", back_populates="showtimes")
