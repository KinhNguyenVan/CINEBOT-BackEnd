from langchain_core.tools import tool, BaseTool
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.service.movie_service import get_now_showing, get_top_movies, get_movies_by_date
from app.service.agent_service.prompts.base import NOW_SHOWING_PROMPT, TOP_MOVIES_PROMPT
from typing import Optional, Type
from pydantic import BaseModel, Field
from datetime import date

class get_now_showing_movies_tool(BaseTool):
    name: str = "get_now_showing_movies"
    description:str = NOW_SHOWING_PROMPT.strip()
    args_schema: Type = None 
    def _run(self, run_manager: Optional[object] = None) -> str:
        db: Session = next(get_db())
        return get_now_showing(db)



class TopMoviesInput(BaseModel):
    limit: int = Field(5,description="Số lượng các bộ phim muốn lấy")
    days: int = Field(7, description="Số ngày gần đây tính từ thời điểm hiện tại để thống kê ")

class get_top_watched_movies_tool(BaseTool):
    name: str = "get_top_watched_movies"
    description: str = TOP_MOVIES_PROMPT.strip()
    args_schema: Type[BaseModel] = TopMoviesInput

    def _run(
        self,
        limit: int = 5,
        days: int = 7,
        run_manager: Optional[object] = None
    ) -> str:
        db: Session = next(get_db())
        return get_top_movies(db, limit, days)


class DateInput(BaseModel):
    day: date = Field(...,description="Số ngày cụ thể theo định dạng YY-MM-DD")

class get_movies_by_date_tool(BaseTool):
    name: str = "get_movies_by_date_tool"
    description: str = "Lấy những bộ phim có suất chiếu trong ngày được cung cấp"
    args_schema: Type[BaseModel] = DateInput

    def _run(self,day,run_manager: Optional[object]=None) -> str:
        db: Session = next(get_db())
        return get_movies_by_date(day= day,db= db)