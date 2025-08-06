from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.ticket import TicketUserInput,GetTicketInput
from app.service.ticket_service import create_ticket,get_ticket
from app.core.database import get_db
from fastapi import BackgroundTasks


router = APIRouter()

@router.post("/tickets/book")
def create_ticket_api(ticket_data: TicketUserInput,background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    return create_ticket(db=db, ticket_data=ticket_data,background_tasks=background_tasks)

@router.post("/tickets/get")
def get_ticket_api(email: GetTicketInput,db:Session = Depends(get_db)):
    return get_ticket(db=db, email = email)
