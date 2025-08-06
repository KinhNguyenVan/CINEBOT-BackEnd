from app.schemas.base import BaseSchema
from pydantic import EmailStr,Field
from typing import Optional


class UserBase(BaseSchema):
    name: str
    year_of_birth: int
    sex: str
    address: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: str  # ma_kh


class UserSession(BaseSchema):
    session_id: str
    email: Optional[EmailStr] = None

class VerifyUserInput(BaseSchema):
    email: EmailStr = Field(...,description="email của người dùng")
    name : str = Field(...,description="Tên của người dùng")