from app.schemas.base import BaseSchema
from datetime import date
from pydantic import EmailStr, Field
from datetime import time, date
from typing import List

class TicketBase(BaseSchema):
    booking_date: date
    email: EmailStr
    showtime_id: str
    seat_id: str

class TicketCreate(TicketBase):
    pass

class Ticket(TicketBase):
    id: str  

class TicketUserInput(BaseSchema):
    email: EmailStr = Field(..., description="Email của người dùng để lấy user_id")
    movie_name: str = Field(..., description="Tên phim mà người dùng muốn xem")
    date_: date = Field(..., description="Ngày chiếu phim")
    time_: time = Field(..., description="Giờ chiếu phim")
    seat_name: List[str] = Field(..., description="Danh sách các ghế mà người dùng chọn")



class GetTicketInput(BaseSchema):
    email: EmailStr = Field(...,description="Email của người dùng")