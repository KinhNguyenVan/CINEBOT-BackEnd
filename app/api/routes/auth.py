from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Header
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.account import Account
from app.models.user import User
from app.schemas.account import AccountCreate
from app.schemas.user import User as UserSchema
from app.auth.auth_handler import hash_password, verify_password, create_access_token,decode_access_token
from app.auth.auth_schema import UserLogin, UserRegister, OTPVerify
from app.utils.id_generator import generate_id
from app.utils.otp import save_otp, verify_otp, send_otp_email,pop_user_data
import random

router = APIRouter()


@router.post("/auth/register")
async def request_register_otp(user: UserRegister, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    existing = db.query(Account).filter(Account.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email đã tồn tại")

    otp = str(random.randint(100000, 999999))
    id = generate_id()

    hashed_pw = hash_password(user.password)

    user_data = {
        "account": {
            "email": user.email,
            "password": hashed_pw,
            "user_id": id
        },
        "user": {
            "id": id,
            "name": user.name,
            "year_of_birth": user.year_of_birth,
            "sex": user.sex,
            "address": user.address
        }
    }

    save_otp(user.email, otp, user_data)

    background_tasks.add_task(send_otp_email, user.email, otp)

    return {"message": "OTP đã được gửi tới email. Vui lòng xác minh."}


@router.post("/auth/verify-otp")
def verify_and_register(data: OTPVerify, db: Session = Depends(get_db)):
    valid, msg = verify_otp(data.email, data.otp)
    if not valid:
        raise HTTPException(status_code=400, detail=msg)

    # Lấy lại data đã lưu từ OTP cache
    cached = pop_user_data(data.email)
    if not cached:
        raise HTTPException(status_code=400, detail="Không tìm thấy dữ liệu người dùng.")

    _, user_data, _ = cached
    account_data = AccountCreate(**user_data["account"])
    user_schema = UserSchema(**user_data["user"])

    user_obj = User(**user_schema.model_dump())
    db.add(user_obj)
    db.flush()

    account_obj = Account(**account_data.model_dump())
    db.add(account_obj)
    db.commit()
    db.refresh(account_obj)

    return {"message": "Tài khoản đã được tạo thành công!"}


@router.post("/auth/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(Account).filter(Account.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Tài khoản hoặc mật khẩu không đúng")

    token = create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}



@router.get("/auth/me")
def get_profile(
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    try:
        scheme, access_token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Scheme không hợp lệ")
        email = decode_access_token(access_token)
        if not email:
            raise HTTPException(status_code=401, detail="Token không hợp lệ")
    except Exception:
        raise HTTPException(status_code=401, detail="Không thể giải mã token")

    account = db.query(Account).filter(Account.email == email).first()
    if not account:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản")

    user = db.query(User).filter(User.id == account.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")

    return {
        "id": user.id,
        "name": user.name,
        "gender": user.sex,
        "address": user.address,
        "birthDate": user.year_of_birth,
        "email": account.email
    }


