"""
response.py

统一 API 返回格式
"""

from typing import Any

from pydantic import BaseModel


class ResponseModel(BaseModel):
    """
    统一响应模型
    """

    code: int = 200
    message: str = "Success"
    data: Any = None


def success(
        data: Any = None,
        message: str = "Success"
) -> ResponseModel:
    """
    成功返回
    """

    return ResponseModel(
        code=200,
        message=message,
        data=data
    )


def fail(
        code: int = 400,
        message: str = "Fail",
        data: Any = None
) -> ResponseModel:
    """
    失败返回
    """

    return ResponseModel(
        code=code,
        message=message,
        data=data
    )