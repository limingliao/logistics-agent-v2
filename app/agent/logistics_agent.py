"""
Enterprise Logistics Agent

职责：
1. 接收用户请求
2. 理解用户意图（Think）
3. 制定执行计划（Plan）
4. 执行任务（Execute）
5. 整理最终回复（Summarize）
"""

from typing import Dict, Any

from sqlalchemy.orm import Session

from app.core.exceptions import BusinessException
from app.core.logger import logger
from app.llm.model import llm
from app.agent.prompts import SYSTEM_PROMPT


class LogisticsAgent:
    """
    企业级 Logistics Agent
    """

    def __init__(self, db: Session):
        self.db = db

    # =====================================================
    # 对外统一入口
    # =====================================================

    def chat(self, message: str) -> str:
        """
        Agent 对话入口
        """

        if not message:
            raise BusinessException("message不能为空")

        logger.info("=" * 60)
        logger.info("[Agent] Start Chat")
        logger.info(f"[User] {message}")

        try:

            # Step1：理解问题
            context = self.think(message)

            # Step2：制定计划
            plan = self.plan(context)

            # Step3：执行
            result = self.execute(plan)

            # Step4：整理回复
            response = self.summarize(result)

            logger.info("[Agent] Chat Finished")

            return response

        except Exception as e:
            logger.exception("[Agent] Chat Failed")
            raise BusinessException("AI服务调用失败") from e

    # =====================================================
    # Think
    # =====================================================

    def think(self, message: str) -> Dict[str, Any]:
        """
        理解用户输入

        后续可以：
        - Intent Recognition
        - Entity Extraction
        - Memory
        """

        logger.info("[Think] Start")

        context = {
            "message": message,
            "intent": None,
            "entities": {}
        }

        logger.info(f"[Think] Context: {context}")

        return context

    # =====================================================
    # Plan
    # =====================================================

    def plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        制定执行计划

        后续这里可以接 Planner。
        """

        logger.info("[Plan] Start")

        plan = {
            "use_tool": False,
            "tool": None,
            "context": context
        }

        logger.info(f"[Plan] {plan}")

        return plan

    # =====================================================
    # Execute
    # =====================================================

    def execute(self, plan: Dict[str, Any]) -> Any:
        """
        执行计划

        当前：
            直接调用 LLM

        后续：
            Tool Dispatcher
            Planner
            Multi Tool
        """

        logger.info("[Execute] Start")

        context = plan["context"]

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": context["message"]
            }
        ]

        result = llm.chat_with_messages(messages)

        logger.info("[Execute] LLM Success")

        return result

    # =====================================================
    # Summarize
    # =====================================================

    def summarize(self, result: Any) -> str:
        """
        整理回复

        后续：
        - Response Formatter
        - Reflection
        - Output Guard
        """

        logger.info("[Summarize] Start")

        if result is None:
            return "暂无结果。"

        return str(result)