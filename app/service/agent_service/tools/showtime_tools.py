from langchain_core.tools import BaseTool
from sqlalchemy.orm import Session
from typing import Optional, Type
from pydantic import BaseModel
from datetime import date
from app.core.database import get_db
from pydantic import Field
from app.service.showtime_service import get_showtimes_by_movie_and_date,get_showtimes_by_date,get_showtimes_by_movie
from app.service.agent_service.prompts.base import SHOWTIMES_BY_MOVIE_NAME_PROMPT

class ShowtimeDetailInput(BaseModel):
    movie_name: str = Field(...,description= "Tên của một bộ phim")
    day: date = Field(...,description="Số ngày cụ thể theo định dạng YYYY-MM-DD")

class ShowtimeDateInput(BaseModel):
    day: date = Field(...,description="Số ngày cụ thể theo định dạng YYYY-MM-DD")

class ShowtimeMovieInput(BaseModel):
    movie_name: str = Field(...,description="Tên của một bộ phim")
    range_day: int =Field(default=7,description="Số ngày thống kê")


class get_showtimes_by_movie_and_date_tool(BaseTool):
    name: str = "get_showtimes_by_movie_and_date_tool"
    description: str = SHOWTIMES_BY_MOVIE_NAME_PROMPT.strip()
    args_schema: Type[BaseModel] = ShowtimeDetailInput

    def _run(
        self,
        movie_name: str,
        day: date,
        run_manager: Optional[object] = None
    ) -> str:
        db: Session = next(get_db())
        return get_showtimes_by_movie_and_date( db, movie_name, day)
    

class get_showtimes_by_date_tool(BaseTool):
    name: str = "get_showtimes_by_date_tool"
    description: str = "Lấy thông tin chi tiết cá suất chiếu có trong ngày được cung cấp"
    args_schema: Type[BaseModel] = ShowtimeDateInput

    def _run(
        self,
        day: date,
        run_manager: Optional[object] = None
    ) -> str:
        db: Session = next(get_db())
        return get_showtimes_by_date( db, day)



class get_showtimes_by_movie_tool(BaseTool):
    name: str = "get_showtimes_by_movie_tool"
    description: str = "Lấy thông tin chi tiết suất chiếu của một bộ phim trong vài ngày tới dựa vào tên bộ phim"
    args_schema: Type[BaseModel] = ShowtimeMovieInput

    def _run(
        self,movie_name: str,
        range_day:int = 5,
        run_manager: Optional[object] = None
    ) -> str:
        db: Session = next(get_db())
        return get_showtimes_by_movie( db, movie_name,range_day)