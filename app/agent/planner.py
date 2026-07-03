"""
Planner V3

职责：
- 基于 context.intent 生成执行计划
- 写入 context.plan
"""

from app.agent.context import AgentContext, PlanStep
from app.core.logger import logger


class Planner:

    def create_plan(self, context: AgentContext) -> AgentContext:
        """
        生成执行计划
        """

        logger.info("[Planner] Start")

        intent = context.intent
        message = context.message

        plan = []

        # =========================
        # ORDER_QUERY
        # =========================
        if intent == "ORDER_QUERY":

            plan.append(
                PlanStep(
                    tool="order_tool",
                    args={"query": message}
                )
            )

        # =========================
        # TRACK_QUERY
        # =========================
        elif intent == "TRACK_QUERY":

            plan.append(
                PlanStep(
                    tool="track_tool",
                    args={"query": message}
                )
            )

        # =========================
        # PRICE_QUERY
        # =========================
        elif intent == "PRICE_QUERY":

            plan.append(
                PlanStep(
                    tool="price_tool",
                    args={"query": message}
                )
            )

        # =========================
        # DEFAULT (LLM fallback)
        # =========================
        else:

            plan.append(
                PlanStep(
                    tool=None,
                    args={}
                )
            )

        context.plan = plan

        logger.info(f"[Planner] Plan size={len(plan)}")

        return context