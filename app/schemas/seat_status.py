from app.schemas.base import BaseSchema

class SeatStatusBase(BaseSchema):
    room_id: str
    seat_id: str

class SeatStatus(SeatStatusBase):
    pass
