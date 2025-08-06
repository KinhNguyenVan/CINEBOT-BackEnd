from sqlalchemy import Column, String, Integer
from app.core.database import Base
from app.utils.id_generator import generate_id
class Room(Base):
    __tablename__ = 'phong_phim'

    id = Column("ma_phong", String, primary_key=True,default=generate_id, index=True)
    name = Column("ten_phong", String)
    seat_count = Column("so_luong_ghe", Integer)