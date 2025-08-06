from sqlalchemy.orm import Session
from app.core.crud import ticket
from app.schemas.ticket import TicketUserInput,GetTicketInput
from fastapi import BackgroundTasks
from typing import Optional
from app.utils.email_sender import send_ticket_email
import asyncio
import threading


def _send_email_thread(email, ticket_infos):
    # Tạo một event loop mới cho thread này
    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)
        # Chạy coroutine đến khi xong
        loop.run_until_complete(send_ticket_email(email, ticket_infos))
    finally:
        loop.close()


def create_ticket(db: Session, ticket_data: TicketUserInput,background_tasks: Optional[BackgroundTasks] = None):
    ticket_infos = ticket.create_ticket_from_user_info(db, ticket_data)
    if background_tasks:
        background_tasks.add_task(send_ticket_email, ticket_data.email, ticket_infos)
    else:
        # tạo một thread daemon để chạy song song, không block trả về
        threading.Thread(
            target=_send_email_thread,
            args=(ticket_data.email, ticket_infos),
            daemon=True
        ).start()

    return {
        "message": "Vé đã được đặt thành công! Sẽ gửi email xác nhận trong vài phút.",
        "tickets": [t["ticket_id"] for t in ticket_infos]
        }

def get_ticket(db:Session,email:GetTicketInput):
    results=ticket.get_ticket_by_email(db,email)
    return results

