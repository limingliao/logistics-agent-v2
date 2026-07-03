"""
Enterprise Logistics Agent

Agent Orchestrator

职责：

1. Think
2. Intent Routing
3. Planning
4. Execution
"""

from typing import Any, Dict

from sqlalchemy.orm import Session

from app.agent.executor import Executor
from app.agent.intent_router import IntentRouter
from app.agent.planner import Planner
from app.agent.prompts import SYSTEM_PROMPT
from app.core.exceptions import BusinessException
from app.core.logger import logger
from app.llm.model import llm
from app.agent.response_formatter import ResponseFormatter
from app.agent.context import AgentContext


class LogisticsAgent:
    """
    企业级 Logistics Agent
    """

    def __init__(self, db: Session):

        self.db = db

        self.router = IntentRouter()

        self.planner = Planner()

        self.executor = Executor()

        self.response_formatter = ResponseFormatter()

    # =====================================================
    # Chat Entry
    # =====================================================

    def chat(self, message: str) -> str:

        if not message:
            raise BusinessException("message不能为空")

        logger.info("=" * 60)
        logger.info("[Agent] Start Chat")
        logger.info(f"[User] {message}")

        try:

            # Step1
            # context = AgentContext(message=message)
            #
            # # Step2
            # context = self.route(context)
            #
            # # Step3
            # plan = self.plan(context)
            #
            # # Step4
            # execution_result = self.execute(plan)
            #
            # # Step5
            # response = self.response_formatter.format(
            #     context=context,
            #     execution_result=execution_result
            # )
            #
            # logger.info("[Agent] Chat Finished")
            #
            # return response
            context = AgentContext(message=message)

            context = self.route(context)

            context = self.plan(context)

            context = self.execute(context)

            context = self.format(context)

            return context.response
        except Exception as e:

            logger.exception("[Agent] Chat Failed")

            raise BusinessException("AI服务调用失败") from e

    # =====================================================
    # Think
    # =====================================================

    # def think(
    #     self,
    #     message: str
    # ) -> Dict[str, Any]:
    #
    #     logger.info("[Think]")
    #
    #     return {
    #
    #         "message": message,
    #
    #         "intent": None,
    #
    #         "entities": {}
    #     }
    def think(self, message: str) -> AgentContext:

        return AgentContext(message=message)

    # =====================================================
    # Route
    # =====================================================

    def route(
        self,
        context: AgentContext
    ) -> AgentContext:

        logger.info("[Router]")

        result = self.router.route(
            context.message
        )

        context.intent = result.intent

        context.entities = result.entities

        context.confidence = result.confidence

        return context

    # =====================================================
    # Plan
    # =====================================================

    def plan(
        self,
        context: AgentContext
    ) -> AgentContext:

        logger.info("[Planner]")

        return self.planner.create_plan(context)

    # =====================================================
    # Execute
    # =====================================================

    def execute(
        self,
        plan: Dict[str, Any]
    ) -> Dict[str, Any]:

        logger.info("[Executor]")

        return self.executor.execute(plan)


    # =====================================================
    # LLM
    # =====================================================

    def chat_with_llm(
        self,
        message: str
    ) -> str:

        logger.info("[LLM]")

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

        return llm.chat_with_messages(messages)