"""
Enterprise Logistics Agent

Agent Orchestrator

职责：

1. Think
2. Intent Routing
3. Planning
4. Execution
5. Summarize
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


class LogisticsAgent:
    """
    企业级 Logistics Agent
    """

    def __init__(self, db: Session):

        self.db = db

        self.router = IntentRouter()

        self.planner = Planner()

        self.executor = Executor()

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
            context = self.think(message)

            # Step2
            context = self.route(context)

            # Step3
            plan = self.plan(context)

            # Step4
            execution_result = self.execute(plan)

            # Step5
            response = self.summarize(
                context=context,
                execution_result=execution_result
            )

            logger.info("[Agent] Chat Finished")

            return response

        except Exception as e:

            logger.exception("[Agent] Chat Failed")

            raise BusinessException("AI服务调用失败") from e

    # =====================================================
    # Think
    # =====================================================

    def think(
        self,
        message: str
    ) -> Dict[str, Any]:

        logger.info("[Think]")

        return {

            "message": message,

            "intent": None,

            "entities": {}
        }

    # =====================================================
    # Route
    # =====================================================

    def route(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:

        logger.info("[Router]")

        result = self.router.route(
            context["message"]
        )

        context["intent"] = result.intent

        context["entities"] = result.entities

        context["confidence"] = result.confidence

        return context

    # =====================================================
    # Plan
    # =====================================================

    def plan(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:

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
    # Summarize
    # =====================================================

    def summarize(
        self,
        context: Dict[str, Any],
        execution_result: Dict[str, Any]
    ) -> str:

        logger.info("[Summarize]")

        # Planner 没有 Tool
        if len(execution_result["results"]) == 0:

            return self.chat_with_llm(
                context["message"]
            )

        # Tool 未命中，回退 LLM
        if execution_result["results"][0]["tool"] == "llm":

            return self.chat_with_llm(
                context["message"]
            )

        # 后续这里可以交给 ResponseFormatter
        return str(execution_result)

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