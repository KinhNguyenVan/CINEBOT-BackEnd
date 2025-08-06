from sqlalchemy import Column, String, ForeignKey
from app.core.database import Base

class SeatStatus(Base):
    __tablename__ = 'trang_thai_ghe'

    room_id = Column("ma_phong", String, ForeignKey("phong_phim.ma_phong"), primary_key=True)
    seat_id = Column("ma_ghe", String, ForeignKey("ghe.ma_ghe"), primary_key=True)