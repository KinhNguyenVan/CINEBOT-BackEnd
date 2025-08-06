from fastapi import APIRouter
from app.service.agent_service.agent_builder import AgentService
from app.utils.generate_session_id_by_email import generate_session_id_by_email
from app.schemas.chat import ChatMessageBase 
from app.service.agent_service.tracing import enable_tracing
from app.schemas.user import UserSession
import uuid
import time

router = APIRouter()

# TTL: 7 phút = 420 giây
AGENT_TTL_SECONDS = 420

# Cấu trúc: session_id -> (AgentService instance, last_access_timestamp)
agent_cache: dict[str, tuple[AgentService, float]] = {}


def clean_agent_cache():
    """Dọn dẹp agent đã hết hạn (không hoạt động quá 7 phút)."""
    now = time.time()
    expired_sessions = [sid for sid, (_, ts) in agent_cache.items() if now - ts > AGENT_TTL_SECONDS]
    for sid in expired_sessions:
        del agent_cache[sid]


@router.post("/chat/agent")
async def chat(message: ChatMessageBase):
    if message.email:
        session_key = generate_session_id_by_email(message.email)
    else:
        session_key = message.session_id

    # Dọn dẹp cache mỗi lần gọi API
    clean_agent_cache()

    # Tìm agent từ cache nếu tồn tại
    if session_key in agent_cache:
        agent, _ = agent_cache[session_key]
    else:
        user = UserSession(session_id=session_key, email=message.email)
        agent = AgentService(user=user)

    # Cập nhật cache (agent + timestamp hiện tại)
    agent_cache[session_key] = (agent, time.time())

    # Gọi agent xử lý tin nhắn
    response = agent.run(message.message)
    return {"response": response}


