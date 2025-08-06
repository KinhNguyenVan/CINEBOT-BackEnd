from sqlalchemy.orm import Session
from sqlalchemy import func, desc, extract
from app.models.showtime import Showtime
from app.models.room import Room
def get_room_by_showtime(db: Session, showtime_id: str):
    result = (
        db.query(Room.name)
        .join(Showtime, Showtime.room_id == Room.id)
        .filter(Showtime.id == showtime_id)
        .first()
    )

    if not result:
        raise "Không tìm thấy thông tin phòng chiếu"
    return result.name