"""
exceptions.py

企业级统一异常定义
"""


class BusinessException(Exception):
    """
    所有业务异常基类
    """

    def __init__(
        self,
        message: str = "业务异常",
        code: int = 400,
    ):
        self.code = code
        self.message = message
        super().__init__(message)


# ======================================================
# Order
# ======================================================

class OrderNotFoundException(BusinessException):
    """
    订单不存在
    """

    def __init__(self):
        super().__init__(
            message="订单不存在",
            code=404
        )


# ======================================================
# User
# ======================================================

class UserNotFoundException(BusinessException):
    """
    用户不存在
    """

    def __init__(self):
        super().__init__(
            message="用户不存在",
            code=404
        )


# ======================================================
# Tool
# ======================================================

class ToolException(BusinessException):
    """
    Tool 调用失败
    """

    def __init__(
        self,
        message: str = "Tool 调用失败"
    ):
        super().__init__(
            message=message,
            code=500
        )


# ======================================================
# Database
# ======================================================

class DatabaseException(BusinessException):
    """
    数据库异常
    """

    def __init__(
        self,
        message: str = "数据库异常"
    ):
        super().__init__(
            message=message,
            code=500
        )


# ======================================================
# Validation
# ======================================================

class ValidationException(BusinessException):
    """
    参数校验失败
    """

    def __init__(
        self,
        message: str = "参数错误"
    ):
        super().__init__(
            message=message,
            code=422
        )


# ======================================================
# Unauthorized
# ======================================================

class UnauthorizedException(BusinessException):
    """
    未授权
    """

    def __init__(
        self,
        message: str = "未授权访问"
    ):
        super().__init__(
            message=message,
            code=401
        )