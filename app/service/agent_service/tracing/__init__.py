import os
from app.core.config import settings

def enable_tracing():
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = settings.LANGCHAIN_API_KEY
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
