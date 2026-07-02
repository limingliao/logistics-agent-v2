"""
聊天接口
"""

from fastapi import APIRouter, HTTPException

from app.core.exceptions import ValidationException
from app.core.logger import logger
from app.core.response import success
from app.database.db import SessionLocal
from app.llm.model import llm
from app.schemas.chat import ChatRequest, ChatResponse
from app.agent.logistics_agent import LogisticsAgent

router = APIRouter()


@router.post(
    "",
    summary="物流智能客服"
)
async def chat(request: ChatRequest):
    # ==========================
    # 参数校验（交给业务异常）
    # ==========================
    if not request.message:
        raise ValidationException("message不能为空")

    logger.info(f"[Chat Request] message={request.message}")

    db = SessionLocal()

    try:
        agent = LogisticsAgent(db=db)
        answer = agent.chat(request.message)

        result = {
            "answer": answer,
            "model": llm.get_model_name()
        }

        logger.info("[Chat Success] response ready")
        return success(result)
    finally:
        db.close()  # 确保会话被关闭
        logger.info("[DB] session closed")