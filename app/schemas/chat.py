from app.schemas.base import BaseSchema
from pydantic import EmailStr
from typing import Optional

class ChatMessageBase(BaseSchema):
    email: Optional[EmailStr] =None
    message: str
    session_id : Optional[str] = None