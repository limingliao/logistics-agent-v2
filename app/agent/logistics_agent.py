from sqlalchemy.orm import Session

from app.core.exceptions import BusinessException
from app.core.logger import logger
from app.llm.model import llm
from app.agent.prompts import SYSTEM_PROMPT
# from app.llm.model import


class LogisticsAgent:

    def __init__(self, db: Session):
        self.db = db

    def chat(self, message: str) -> str:
        """
        AI 对话入口
        """
        if not message:
            raise BusinessException("message不能为空")
        logger.info(f"[LogisticsAgent] input: {message}")

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


        # return llm.chat_with_tools()

        try:
            result = llm.chat_with_messages(messages)

            logger.info("[LogisticsAgent] llm call success")

            return result

        except Exception as e:
            logger.exception("[LogisticsAgent] llm call failed")
            raise BusinessException("AI服务调用失败") from e