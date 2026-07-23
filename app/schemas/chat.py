"""
聊天请求/响应数据模型
"""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    用户请求
    """

    message: str = Field(
        ...,
        description="用户输入内容",
        example="帮我查一下订单 SF123456"
    )


class ChatResponse(BaseModel):

    success: bool = True

    answer: str

    model: str = ""

    elapsed: float = 0