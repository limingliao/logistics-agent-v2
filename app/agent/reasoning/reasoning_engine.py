"""
Reasoning Engine
"""

from app.agent.reasoning.reasoning_result import (
    ReasoningResult,
    ReasoningTask
)


class ReasoningEngine:

    """
    企业级推理引擎

    V1：

    Task排序

    V2：

    DAG

    V3：

    Graph Planning
    """

    def reason(
        self,
        tasks: list[ReasoningTask]
    ) -> ReasoningResult:

        result = ReasoningResult()

        result.tasks = tasks

        for task in tasks:

            result.reasoning_trace.append(

                f"Create Task -> {task.name}"

            )

        result.message = "Reasoning Success"

        return result