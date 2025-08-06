from app.schemas.base import BaseSchema

class RoomBase(BaseSchema):
    name: str
    seat_count: int

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: str  # ma_phong