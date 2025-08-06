from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.account import Account
from app.auth.auth_handler import hash_password, verify_password, create_access_token
from app.auth.auth_schema import UserLogin, UserRegister, OTPVerify
from app.utils.otp import generate_otp, save_otp, verify_otp, send_otp_email

router = APIRouter()

@router.post("/auth/register")
async def request_register_otp(user: UserRegister, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    existing = db.query(Account).filter(Account.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email đã được đăng ký.")

    otp = generate_otp()
    save_otp(user.email, otp)
    background_tasks.add_task(send_otp_email, user.email, otp)
    return {"message": "Đã gửi mã OTP tới email. Vui lòng xác minh."}


@router.post("/auth/verify-otp")
def verify_otp_register(req: OTPVerify):
    valid, msg = verify_otp(req.email, req.otp)
    if not valid:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg}


@router.post("/auth/register/confirm")
def confirm_register(user: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(Account).filter(Account.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email đã được đăng ký.")

    hashed_pw = hash_password(user.password)
    new_user = Account(email=user.email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    return {"message": "Tạo tài khoản thành công"}


@router.post("/auth/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(Account).filter(Account.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}
