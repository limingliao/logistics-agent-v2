"""
聊天接口
"""

from fastapi import APIRouter

from app.core.exceptions import ValidationException
from app.core.logger import logger
from app.core.response import success

from app.schemas.chat import (
    ChatRequest,
    ChatResponse
)

from app.agent.agent_manager import AgentManager


router = APIRouter()


# 临时全局
# 后续迁移到依赖注入
agent_manager: AgentManager = None



def set_agent_manager(
    manager: AgentManager
):

    global agent_manager

    agent_manager = manager



@router.post(
    "",
    summary="物流智能客服"
)
async def chat(
    request: ChatRequest
):

    if not request.message:

        raise ValidationException(
            "message不能为空"
        )


    logger.info(
        f"[Chat Request] {request.message}"
    )


    if agent_manager is None:

        return success({

            "answer":
                "Agent未初始化"

        })


    result = agent_manager.run(

        message=request.message

    )


    return success({

        "answer":
            result.text,

        "model":
            result.model,

        "elapsed":
            result.elapsed

    })