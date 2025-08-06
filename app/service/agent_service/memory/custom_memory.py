from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseMessage, SystemMessage
from typing import List, Dict, Any
import logging
from pydantic import Field



class CustomSystemPromptMemory(ConversationBufferMemory):
    # Định nghĩa fields cho Pydantic
    system_prompt: str = Field(default="You are a helpful assistant.")
    max_history: int = Field(default=20)

    def __init__(self, system_prompt: str, max_history: int = 20, **kwargs):
        super().__init__(
            system_prompt=system_prompt,
            max_history=max_history,
            **kwargs
        )

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Load memory variables with system prompt and trimmed history"""
        try:
            history: List[BaseMessage] = self.chat_memory.messages
            
            trimmed_history = history[-self.max_history:] if len(history) > self.max_history else history
            
            messages = [SystemMessage(content=self.system_prompt)] + trimmed_history
            
            return {self.memory_key: messages}
            
        except Exception as e:
            return {self.memory_key: [SystemMessage(content=self.system_prompt)]}

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        """Save context to memory"""
        try:
            super().save_context(inputs, outputs)
        except Exception as e:
            print(f"Error saving context: {e}")

    def clear(self) -> None:
        """Clear memory"""
        try:
            self.chat_memory.clear()
            print("Memory cleared successfully")
        except Exception as e:
            print(f"Error clearing memory: {e}")
