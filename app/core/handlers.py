"""
handlers.py

全局异常处理
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import BusinessException
from app.core.logger import logger


def register_exception_handlers(app: FastAPI):
    """
    注册全局异常处理器
    """

    # ======================================================
    # Business Exception
    # ======================================================

    @app.exception_handler(BusinessException)
    async def business_exception_handler(
        request: Request,
        exc: BusinessException,
    ):
        logger.warning(
            f"[BusinessException] {request.method} {request.url.path} -> {exc.message}"
        )

        return JSONResponse(
            status_code=200,
            content={
                "code": exc.code,
                "message": exc.message,
                "data": None
            }
        )

    # ======================================================
    # Unknown Exception
    # ======================================================

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception,
    ):
        logger.exception(
            f"[Unhandled Exception] {request.method} {request.url.path}"
        )

        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "message": "服务器内部错误",
                "data": None
            }
        )