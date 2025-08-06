from sqlalchemy import Column, String, Text
from app.core.database import Base
from app.utils.id_generator import generate_id
class Movie(Base):
    __tablename__ = 'phim'

    id = Column("ma_phim", String, primary_key=True,default=generate_id, index=True)
    name = Column("ten_phim", String)
    nsx = Column("NSX", String)
    actors = Column("nhan", Text)
    genre = Column("the_loai", String)
    poster = Column("poster",Text)
