"""
main.py

物流智能客服 Agent
项目启动入口
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.core.handlers import register_exception_handlers
from app.core.middleware import register_middleware
from app.core.logger import logger


def create_agent_manager():
    pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    """

    logger.info("=" * 50)
    logger.info("🚀 Logistics AI Agent 正在启动...")
    logger.info("running on:http://127.0.0.1:8000")
    logger.info("running on(docs):http://127.0.0.1:8000/docs")

    logger.info("=" * 50)
 
    # 初始化Agent
    manager = create_agent_manager()


    # 注入chat接口
    set_agent_manager(
        manager
    )
    yield

    logger.info("=" * 50)
    logger.info("👋 Logistics AI Agent 已关闭")
    logger.info("=" * 50)


app = FastAPI(
    title="物流行业智能客服 Agent",
    description="基于 FastAPI + Python + LLM 构建的物流客服系统",
    version="2.0.0",
    lifespan=lifespan,
)

register_exception_handlers(app)

register_middleware(app)

@app.get("/")
async def home():
    """
    首页
    """
    return {
        "project": "Logistics AI Agent",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
async def health():
    """
    健康检查
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": "ok",
            "message": "Service is running"
        }
    )


@app.get("/ping")
async def ping():
    """
    Ping接口
    """
    return {
        "message": "pong"
    }


# ==========================
# 注册路由
# ==========================

# 后续开发时取消注释即可
#
from app.api.chat import router as chat_router, set_agent_manager

# from app.api.order import router as order_router
#
app.include_router(chat_router, prefix="/chat", tags=["聊天"])
# app.include_router(order_router, prefix="/order", tags=["订单"])

# from app.core.logger import logger
#
# logger.info("项目启动成功")
# logger.warning("这是一个警告")
# logger.error("这是一个错误")

# from app.core.exceptions import OrderNotFoundException
#
# @app.get("/test")
# def test():
#
#     raise OrderNotFoundException()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )