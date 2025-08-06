from pydantic import BaseModel,EmailStr,Field
from app.schemas.user import VerifyUserInput
from fastapi import BackgroundTasks
from typing import Optional
from sqlalchemy.orm import Session
from app.models.account import Account
from app.models.user import User
from app.utils.otp import verify_otp as verify_otp_func,save_otp, send_otp_email,pop_user_data
import random
from app.auth.auth_handler import hash_password

def verify_email(
    db: Session,
    user_input: VerifyUserInput,
    background_tasks: Optional[BackgroundTasks] = None
):
    email = user_input.email

    # Kiểm tra email đã tồn tại trong hệ thống chưa
    existing_account = db.query(Account).filter(Account.email == email).first()
    if existing_account:
        return {"status": "success", "message": "Email đã tồn tại trong hệ thống."}

    # Nếu chưa tồn tại, sinh mã OTP và gửi email
    otp = otp = str(random.randint(100000, 999999))
    save_otp(email, otp, user_data={"name":user_input.name})

    if background_tasks:
        background_tasks.add_task(send_otp_email, email, otp)
    else:
        # Nếu không dùng BackgroundTasks thì gửi trực tiếp
        import asyncio
        asyncio.create_task(send_otp_email(email, otp))

    return {
        "status": "pending",
        "message": f"Đã gửi mã OTP tới email: {email}. Vui lòng kiểm tra và xác nhận."
    }



class OTPVerifyInput(BaseModel):
    email: EmailStr = Field(...,description="email của người dùng")
    otp: str = Field(...,description="otp của người dùng nhập được nhận từ hệ thống")

def verify_OTP(db: Session, user_input: OTPVerifyInput) -> str:
    success, message = verify_otp_func(user_input.email, user_input.otp)
    if not success:
        return f"Xác minh thất bại: {message}"

    cached = pop_user_data(user_input.email)
    if not cached:
        return "Không tìm thấy thông tin người dùng trong cache."
    
    _, user_data, _ = cached

    # Kiểm tra lại
    if db.query(Account).filter_by(email=user_input.email).first():
        return "Tài khoản đã tồn tại."

    # Tạo User
    new_user = User(
        name=user_data["name"],
        year_of_birth=None,
        sex=None,
        address=None
    )
    db.add(new_user)
    db.flush()  # Lấy ID của user mới

    # Tạo Account (không có mật khẩu vì chỉ xác minh OTP)
    new_password = hash_password("@Test123")
    new_account = Account(
        email=user_input.email,
        password=new_password,
        user_id=new_user.id
    )
    db.add(new_account)
    db.commit()

    return "Xác minh OTP thành công. Tài khoản đã được tạo với mật khẩu mặc định là @Test123."
   