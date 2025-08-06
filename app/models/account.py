from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.utils.id_generator import generate_id

class Account(Base):
    __tablename__ = 'tai_khoan'

    email = Column("email", String, primary_key=True, index=True)
    password = Column("mat_khau", String)
    user_id = Column("ma_kh", String, ForeignKey("khach_hang.ma_kh"))

