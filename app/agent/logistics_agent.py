from sqlalchemy.orm import Session

from app.llm.model import llm
from app.agent.prompts import SYSTEM_PROMPT
# from app.llm.model import chat_with_tools


class LogisticsAgent:

    def __init__(self, db: Session):
        self.db = db

    def chat(self, message: str) -> str:
        """
        AI 对话入口
        """

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": message
            }
        ]


        # return llm.chat_with_messages(messages)
        return llm.chat_with_tools()