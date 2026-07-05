"""
Reasoning Manager
"""

from app.agent.reasoning.reasoning_engine import (
    ReasoningEngine
)

from app.agent.reasoning.task_parser import (
    TaskParser
)

from app.agent.reasoning.reasoning_result import (
    ReasoningResult
)


class ReasoningManager:

    """
    企业级 Reasoning Manager
    """

    def __init__(self):

        self.parser = TaskParser()

        self.engine = ReasoningEngine()

    def run(
        self,
        message: str,
        intent: str
    ) -> ReasoningResult:

        tasks = self.parser.parse(
            message,
            intent
        )

        result = self.engine.reason(tasks)

        return result