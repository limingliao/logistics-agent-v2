"""
Workflow Context

Workflow运行期间共享的数据上下文
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class WorkflowContext:
    """
    Workflow共享上下文
    """

    workflow_id: str

    question: str

    conversation_id: Optional[str] = None

    user_id: Optional[str] = None

    history: List[Any] = field(default_factory=list)

    memories: List[Any] = field(default_factory=list)

    reasoning_result: Optional[Any] = None

    tool_results: List[Any] = field(default_factory=list)

    variables: Dict[str, Any] = field(default_factory=dict)

    shared_data: Dict[str, Any] = field(default_factory=dict)

    metadata: Dict[str, Any] = field(default_factory=dict)

    current_step: Optional[str] = None

    completed_steps: List[str] = field(default_factory=list)

    failed_steps: List[str] = field(default_factory=list)

    logs: List[str] = field(default_factory=list)

    final_answer: Optional[str] = None

    def set_variable(self, key: str, value: Any) -> None:
        """设置变量"""

        self.variables[key] = value

    def get_variable(self, key: str, default=None):
        """获取变量"""

        return self.variables.get(key, default)

    def has_variable(self, key: str) -> bool:
        """变量是否存在"""

        return key in self.variables

    def remove_variable(self, key: str) -> None:
        """删除变量"""

        self.variables.pop(key, None)

    def add_tool_result(self, result: Any) -> None:
        """新增Tool执行结果"""

        self.tool_results.append(result)

    def add_memory(self, memory: Any) -> None:
        """新增Memory"""

        self.memories.append(memory)

    def add_history(self, message: Any) -> None:
        """新增历史消息"""

        self.history.append(message)

    def add_log(self, message: str) -> None:
        """新增日志"""

        self.logs.append(message)

    def mark_step_completed(self, step_id: str) -> None:
        """标记Step完成"""

        if step_id not in self.completed_steps:
            self.completed_steps.append(step_id)

    def mark_step_failed(self, step_id: str) -> None:
        """标记Step失败"""

        if step_id not in self.failed_steps:
            self.failed_steps.append(step_id)

    def reset_runtime(self) -> None:
        """
        清理运行状态
        """

        self.current_step = None

        self.completed_steps.clear()

        self.failed_steps.clear()

        self.logs.clear()

        self.tool_results.clear()

        self.final_answer = None

    def to_dict(self) -> Dict[str, Any]:
        """
        序列化
        """

        return {
            "workflow_id": self.workflow_id,
            "conversation_id": self.conversation_id,
            "user_id": self.user_id,
            "question": self.question,
            "variables": self.variables,
            "shared_data": self.shared_data,
            "metadata": self.metadata,
            "completed_steps": self.completed_steps,
            "failed_steps": self.failed_steps,
            "current_step": self.current_step,
            "final_answer": self.final_answer,
        }