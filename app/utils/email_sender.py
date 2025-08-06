from email.message import EmailMessage
from app.core.config import settings
import aiosmtplib
from typing import List
async def send_ticket_email(to_email: str, ticket_infos: List[dict]):
    body = "🎬 THÔNG TIN VÉ CỦA BẠN 🎫\n\n"

    for ticket in ticket_infos:
        body += f"""Mã vé: {ticket['ticket_id']}
Tên phim: {ticket['movie_name']}
Ngày chiếu: {ticket['date']}
Giờ chiếu: {ticket['time']}
Ghế: {ticket['seat_name']}
Phòng chiếu: {ticket['room_name']}
Ngày đặt: {ticket['booking_date']}

"""

    body += "Cảm ơn bạn đã đặt vé tại hệ thống của chúng tôi!"

    msg = EmailMessage()
    msg["From"] = settings.SMTP_USERNAME
    msg["To"] = to_email
    msg["Subject"] = "Xác nhận vé xem phim"
    msg.set_content(body)

    await aiosmtplib.send(
        msg,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        start_tls=True,
        username=settings.SMTP_USERNAME,
        password=settings.SMTP_PASSWORD
    )
