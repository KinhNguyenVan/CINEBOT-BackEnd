from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.utils.id_generator import generate_id
class User(Base):
    __tablename__ = 'khach_hang'

    id = Column("ma_kh", String, primary_key=True, index=True, default=generate_id)
    name = Column("ten", String)
    year_of_birth = Column("nam_sinh", Integer)
    sex = Column("gioi_tinh", String)
    address = Column("dia_chi", String)

