from app.service.agent_service.llm_provider.base import LLMProvider
from app.core.config import settings
from langchain_google_genai import ChatGoogleGenerativeAI

class GeminiProvider(LLMProvider):
    def get_llm(self):
        raw_llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=settings.GEMINI_API_KEY,
            temperature=1.2
        )
        return raw_llm


