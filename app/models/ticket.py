from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.utils.id_generator import generate_id

class Ticket(Base):
    __tablename__ = 've'

    id = Column("ma_ve", String, primary_key=True, index=True, default=generate_id)
    booking_date = Column("ngay_dat", Date)
    email = Column("email", String, ForeignKey("tai_khoan.email"))
    showtime_id = Column("ma_lich_chieu", String, ForeignKey("lich_chieu.ma_lich_chieu"))
    seat_id = Column("ma_ghe", String, ForeignKey("ghe.ma_ghe"))

