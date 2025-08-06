from langchain_core.tools import tool, BaseTool
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.service.seat_service import get_available_seats
from typing import Optional, Type
from pydantic import BaseModel, Field
from datetime import date, time


class QuerySeatAvailableInput(BaseModel):
    movie_name: str = Field(...,description="Tên của một bộ phim")
    show_date: date = Field(...,description="Ngày có suất chiếu phim (YYYY-MM-DD)")
    show_time :time = Field(...,description="Thời gian bắt đầu suất chiếu phim trong ngày (HH:MM)")

class get_seats_available_tool(BaseTool):
    name: str = "get_seats_available"
    description: str = "Lấy ra tất cả các ghế còn trống trong một suất chiếu phim khi biết tên phim, ngày và giờ suất chiếu"
    args_schema: Type[BaseModel] = QuerySeatAvailableInput
    def _run(self,movie_name:str,show_date:date,show_time:time, run_manager: Optional[object] = None):
        db: Session = next(get_db())
        return get_available_seats(db,movie_name,show_date,show_time)