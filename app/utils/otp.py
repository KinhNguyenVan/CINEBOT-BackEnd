import random, time
from email.message import EmailMessage
import aiosmtplib
from app.core.config import settings

otp_cache = {}


def generate_otp():
    return str(random.randint(100000, 999999))

def save_otp(email: str, otp: str, user_data: dict, ttl=300):
    expire = time.time() + ttl
    otp_cache[email] = (otp, user_data, expire)

def get_cached_user(email: str):
    return otp_cache.get(email)

def verify_otp(email: str, input_otp: str):
    if email not in otp_cache:
        return False, "Không tìm thấy OTP"
    otp, _, expire = otp_cache[email]
    if time.time() > expire:
        del otp_cache[email]
        return False, "OTP đã hết hạn"
    if otp != input_otp:
        return False, "OTP không đúng"
    return True, "OTP hợp lệ"

def pop_user_data(email: str):
    return otp_cache.pop(email, None)

async def send_otp_email(email: str, otp: str):
    msg = EmailMessage()
    msg["From"] = settings.SMTP_USERNAME
    msg["To"] = email
    msg["Subject"] = "Mã OTP xác minh đăng ký"
    msg.set_content(f"Mã OTP của bạn là: {otp}")

    await aiosmtplib.send(
        msg,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        start_tls=True,
        username=settings.SMTP_USERNAME,
        password=settings.SMTP_PASSWORD
    )

def pop_user_data(email: str):
    return otp_cache.pop(email, None)
