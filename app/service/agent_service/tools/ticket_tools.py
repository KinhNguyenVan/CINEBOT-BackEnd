from langchain_core.tools import BaseTool
from app.service.ticket_service import create_ticket,get_ticket
from app.schemas.ticket import TicketUserInput, GetTicketInput
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.service.agent_service.prompts.base import CREATE_TICKET_PROMPT
from typing import  Type
from pydantic import BaseModel,EmailStr


class create_ticket_tool(BaseTool):
    name: str = "create_ticket_tool"
    description: str = CREATE_TICKET_PROMPT.strip()
    args_schema: Type[BaseModel] = TicketUserInput

    def _run(self,**kwargs) -> str:
        ticket_data = TicketUserInput(**kwargs) 
        db: Session = next(get_db())
        return create_ticket(db, ticket_data)

class get_ticket_tool(BaseTool):
    name:str = "get_ticket_tool"
    description :str = "Lấy tất cả các vé xem phim đã được đặt dựa vào email của người dùng cung cấp"
    args_schema: Type[BaseModel] = GetTicketInput

    def _run(self,email: EmailStr,**kwargs):
        db :Session = next(get_db())
        results = get_ticket(db,email)
        if len(results) == 0:
            return f"Người dùng với email: {email} chưa đặt vé nào"
        return get_ticket(db,email)