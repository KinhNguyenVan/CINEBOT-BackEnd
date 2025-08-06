from app.schemas.base import BaseSchema

class MovieBase(BaseSchema):
    name: str
    nsx: str
    actors: str
    genre: str

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: str  # ma_phim
