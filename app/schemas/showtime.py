from app.schemas.base import BaseSchema
from datetime import time, date

class ShowtimeBase(BaseSchema):
    time: time
    date: date
    movie_id: str
    room_id: str

class ShowtimeCreate(ShowtimeBase):
    pass

class Showtime(ShowtimeBase):
    id: str  # ma_lich_chieu