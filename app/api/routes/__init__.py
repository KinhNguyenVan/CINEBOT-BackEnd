from fastapi import APIRouter
from .auth import router as auth_routes
from .movie import router as movie_routes
from .ticket import router as ticket_routes
from .showtime import router as showtime_routes
from .agent_chat import router as agent_chat_routes

api_router = APIRouter()
api_router.include_router(auth_routes)
api_router.include_router(movie_routes)
api_router.include_router(ticket_routes)
api_router.include_router(showtime_routes)
api_router.include_router(agent_chat_routes)

