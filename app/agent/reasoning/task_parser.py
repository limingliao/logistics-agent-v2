"""
Task Parser

负责将自然语言拆解成多个Task
"""

from app.agent.reasoning.reasoning_result import (
    ReasoningTask
)


class TaskParser:

    """
    Rule-Based Task Parser
    """

    def parse(
        self,
        message: str,
        intent: str
    ) -> list[ReasoningTask]:

        tasks = []

        if intent == "ORDER_QUERY":

            tasks.append(
                ReasoningTask(
                    name="查询订单",
                    intent=intent,
                    tool="order_tool",
                    args={
                        "query": message
                    }
                )
            )

        elif intent == "TRACK_QUERY":

            tasks.append(
                ReasoningTask(
                    name="查询物流",
                    intent=intent,
                    tool="track_tool",
                    args={
                        "query": message
                    }
                )
            )

        elif intent == "PRICE_QUERY":

            tasks.append(
                ReasoningTask(
                    name="查询运费",
                    intent=intent,
                    tool="price_tool",
                    args={
                        "query": message
                    }
                )
            )

        else:

            tasks.append(
                ReasoningTask(
                    name="LLM回答",
                    intent=intent,
                    tool=None
                )
            )

        return tasks