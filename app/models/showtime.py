from sqlalchemy import Column, String, Time, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.utils.id_generator import generate_id

class Showtime(Base):
    __tablename__ = 'lich_chieu'

    id = Column("ma_lich_chieu", String, primary_key=True,default=generate_id, index=True)
    time = Column("gio", Time)
    date = Column("ngay", Date)
    movie_id = Column("ma_phim", String, ForeignKey("phim.ma_phim"))
    room_id = Column("ma_phong", String, ForeignKey("phong_phim.ma_phong"))
