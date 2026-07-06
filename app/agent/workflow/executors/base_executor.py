from abc import ABC, abstractmethod
from typing import Any

from app.agent.workflow.workflow_context import WorkflowContext
from app.agent.workflow.workflow_step import WorkflowStep


class BaseExecutor(ABC):
    """
    所有Executor基类
    """

    @abstractmethod
    def execute(
        self,
        step: WorkflowStep,
        context: WorkflowContext,
    ) -> Any:
        """
        执行Step
        """
        pass