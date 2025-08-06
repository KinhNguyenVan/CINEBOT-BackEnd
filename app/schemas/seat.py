from app.schemas.base import BaseSchema

class SeatBase(BaseSchema):
    name: str

class SeatCreate(SeatBase):
    pass

class Seat(SeatBase):
    id: str  # ma_ghe
