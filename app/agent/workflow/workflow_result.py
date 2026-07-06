"""
Workflow Result

保存整个 Workflow 的最终执行结果
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from .workflow_state import WorkflowState


@dataclass
class WorkflowResult:
    """
    Workflow执行结果
    """

    workflow_id: str

    success: bool = False

    state: WorkflowState = WorkflowState.CREATED

    answer: str = ""

    output: Any = None

    error: Optional[str] = None

    tool_results: List[Dict[str, Any]] = field(default_factory=list)

    step_results: List[Dict[str, Any]] = field(default_factory=list)

    variables: Dict[str, Any] = field(default_factory=dict)

    metadata: Dict[str, Any] = field(default_factory=dict)

    started_at: Optional[datetime] = None

    finished_at: Optional[datetime] = None

    duration: float = 0.0

    token_usage: Dict[str, int] = field(default_factory=dict)

    def add_step_result(self, result: Dict[str, Any]) -> None:
        """新增Step执行结果"""

        self.step_results.append(result)

    def add_tool_result(self, result: Dict[str, Any]) -> None:
        """新增Tool结果"""

        self.tool_results.append(result)

    def set_variable(self, key: str, value: Any) -> None:
        """保存变量"""

        self.variables[key] = value

    def get_variable(self, key: str, default=None):
        """获取变量"""

        return self.variables.get(key, default)

    def finish(
        self,
        success: bool,
        answer: str = "",
        error: Optional[str] = None,
    ) -> None:
        """结束Workflow"""

        self.success = success

        self.answer = answer

        self.error = error

        self.finished_at = datetime.utcnow()

        if self.started_at:

            self.duration = (
                self.finished_at - self.started_at
            ).total_seconds()

        self.state = (
            WorkflowState.SUCCESS
            if success
            else WorkflowState.FAILED
        )