from app.service.agent_service.llm_provider.factory import GeminiProvider
from app.service.agent_service.memory.chat_history import get_postgres_memory
from app.service.agent_service.prompts.base import SYSTEM_PROMPT,SYSTEM_PROMPT_NEW
from app.service.agent_service.tools.ticket_tools import create_ticket_tool,get_ticket_tool
from app.service.agent_service.tools.showtime_tools import get_showtimes_by_movie_and_date_tool,get_showtimes_by_date_tool,get_showtimes_by_movie_tool
from app.service.agent_service.tools.movie_tools import get_now_showing_movies_tool, get_top_watched_movies_tool,get_movies_by_date_tool
from app.service.agent_service.tools.seat_tools import get_seats_available_tool
from app.service.agent_service.tools.auth_tool import verify_otp_tool, send_otp_tool
from langchain.agents import AgentExecutor,create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.schema import SystemMessage
from app.service.agent_service.memory.custom_memory import CustomSystemPromptMemory
from app.schemas.user import UserSession
import logging
from app.utils.get_current_time import get_current_time


class AgentService:
    def __init__(self, user: UserSession):
        self.session_id = user.session_id
        self.memory = get_postgres_memory(self.session_id)
        self.system_prompt = SYSTEM_PROMPT_NEW.format(email = user.email,time = get_current_time())
        self.chat_history = CustomSystemPromptMemory(
            memory_key="chat_history",
            chat_memory=self.memory.chat_memory,
            return_messages=True,
            max_history=20,
            system_prompt=self.system_prompt
            )
        self.llm_provider = GeminiProvider()
        self.tools = [
            create_ticket_tool(),
            get_showtimes_by_movie_and_date_tool(),
            get_now_showing_movies_tool(),
            get_top_watched_movies_tool(),
            get_movies_by_date_tool(),
            get_showtimes_by_date_tool(),
            get_seats_available_tool(),
            get_showtimes_by_movie_tool(),
            get_ticket_tool(),
            verify_otp_tool(),
            send_otp_tool(),
        ]

        self.agent = self._create_openai_function_agent()

    def _create_openai_function_agent(self) -> AgentExecutor:
        try:
            llm = self.llm_provider.get_llm()
            prompt = ChatPromptTemplate(
                input_variables=["input", "chat_history", "agent_scratchpad"],
                messages=[
                    SystemMessage(content=self.system_prompt),
                    MessagesPlaceholder(variable_name="chat_history"),
                    HumanMessagePromptTemplate.from_template("{input}"),
                    MessagesPlaceholder(variable_name="agent_scratchpad")
                ]
            )

            agent = create_openai_tools_agent(
                llm=llm,
                tools=self.tools,
                prompt=prompt
            )
            return AgentExecutor.from_agent_and_tools(
                agent=agent,
                tools=self.tools,
                memory=self.chat_history,
                verbose=False,
                handle_parsing_errors=True,
                max_iterations=50,
                max_execution_time=40,
            )
        except Exception as e:
            logging.error(f"Error creating OpenAI function agent: {e}")
            raise   

    def run(self, message: str) -> str:
        try:
            result = self.agent.invoke({"input": message})
            return result.get("output", "Xin lỗi, tôi không thể xử lý yêu cầu này.")
        except Exception as e:
            logging.error(f"Error processing message: {e}")
            return "Xin lỗi, có lỗi xảy ra. Vui lòng thử lại."