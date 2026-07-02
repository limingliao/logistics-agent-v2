"""
model.py

统一封装 LLM 调用
"""


from openai import OpenAI

from app.agent.prompts import SYSTEM_PROMPT
from app.config.settings import settings


class LLMModel:

    def __init__(self):

        self.api_key = settings.DEEPSEEK_API_KEY

        if not self.api_key:
            raise ValueError("请配置 DEEPSEEK_API_KEY")

        self.base_url = settings.DEEPSEEK_BASE_URL

        self.model = settings.MODEL_NAME

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    # =====================================================
    # 普通聊天
    # =====================================================

    def chat(self, message: str):

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

        return self.chat_with_messages(messages)

    # =====================================================
    # 多轮聊天
    # =====================================================

    def chat_with_messages(self, messages):

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.3,
            messages=messages,
        )

        return response.choices[0].message.content

    # =====================================================
    # Tool Calling
    # =====================================================

    def chat_with_tools(
            self,
            messages,
            tools,
    ):
        """
        支持 Tool Calling
        """

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.3,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

    # =====================================================
    # 当前模型
    # =====================================================

    def get_model_name(self):

        return self.model


llm = LLMModel()