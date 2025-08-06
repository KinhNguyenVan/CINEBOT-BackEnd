from app.schemas.base import BaseSchema

class AccountBase(BaseSchema):
    email: str
    password: str
    user_id: str  # ma_kh

class AccountCreate(AccountBase):
    pass

class Account(AccountBase):
    pass