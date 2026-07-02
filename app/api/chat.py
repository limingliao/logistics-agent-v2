"""
聊天接口
"""

from fastapi import APIRouter, HTTPException

from app.database.db import SessionLocal
from app.llm.model import llm
from app.schemas.chat import ChatRequest, ChatResponse
from app.agent.logistics_agent import LogisticsAgent

router = APIRouter()


@router.post(
    "",
    response_model=ChatResponse,
    summary="物流智能客服"
)
async def chat(request: ChatRequest):
    """
    AI聊天接口
    """
    db = SessionLocal()

    try:
        agent = LogisticsAgent(db=db)
        answer = agent.chat(request.message)

        return ChatResponse(
            success=True,
            answer=answer,
            model=llm.get_model_name()
        )

    except Exception as e:
        # 记录日志（可选）
        # logger.error(f"Chat error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    finally:
        db.close()  # 确保会话被关闭