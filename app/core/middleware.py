"""
middleware.py

企业级全局中间件
"""

import time

from fastapi import FastAPI, Request

from app.core.logger import logger


def register_middleware(app: FastAPI):
    """
    注册全局中间件
    """

    @app.middleware("http")
    async def log_requests(request: Request, call_next):

        start_time = time.perf_counter()

        logger.info(
            f"--> {request.method} {request.url.path}"
        )

        response = await call_next(request)

        process_time = (time.perf_counter() - start_time) * 1000

        logger.info(
            f"<-- {request.method} {request.url.path} "
            f"{response.status_code} "
            f"{process_time:.2f} ms"
        )

        return response