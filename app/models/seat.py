from sqlalchemy import Column, String
from app.core.database import Base
from app.utils.id_generator import generate_id
class Seat(Base):
    __tablename__ = 'ghe'

    id = Column("ma_ghe", String, primary_key=True,default=generate_id, index=True)
    name = Column("ten_ghe", String)