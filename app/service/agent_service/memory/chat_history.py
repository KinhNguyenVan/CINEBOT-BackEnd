from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import PostgresChatMessageHistory
from app.core.config import settings
import psycopg  

def get_postgres_memory(session_id: str) -> ConversationBufferMemory:
    """Create PostgreSQL-backed conversation memory safely"""
    
    # Tạo kết nối và đảm bảo nó tự đóng sau khi khởi tạo xong
    message_history = PostgresChatMessageHistory(
        table_name="message_database",   
        session_id=session_id,
        connection_string=settings.DATABASE_URL,
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        chat_memory=message_history,
        return_messages=True
    )

    return memory