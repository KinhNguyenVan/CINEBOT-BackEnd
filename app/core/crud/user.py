from app.models.account import Account 
from sqlalchemy.orm import Session
from fastapi import HTTPException

def get_user_id_by_email(db: Session, email: str) -> str:
    user = db.query(Account).filter(Account.email == email).first()

    if not user:
        return f"Không tìm thấy người dùng với email {email}"

    return user.user_id