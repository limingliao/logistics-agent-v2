"""
Workflow

企业级 Workflow 定义。

职责：

- 保存 Workflow 信息
- 保存所有 WorkflowStep
- 管理 Workflow 生命周期
- 提供 Step 查询接口
- 判断 Workflow 是否完成
- 为 WorkflowEngine 提供执行对象
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from app.agent.workflow.workflow_context import WorkflowContext
from app.agent.workflow.workflow_state import WorkflowState
from app.agent.workflow.workflow_step import WorkflowStep


@dataclass
class Workflow:
    """
    企业级 Workflow
    """

    # ==========================================================
    # 基础信息
    # ==========================================================

    workflow_id: str

    name: str

    description: str = ""

    # ==========================================================
    # Context
    # ==========================================================

    context: Optional[WorkflowContext] = None

    # ==========================================================
    # Steps
    # ==========================================================

    steps: List[WorkflowStep] = field(default_factory=list)

    # ==========================================================
    # Runtime
    # ==========================================================

    state: WorkflowState = WorkflowState.CREATED

    current_step_index: int = -1

    metadata: Dict[str, Any] = field(default_factory=dict)

    created_at: datetime = field(default_factory=datetime.utcnow)

    updated_at: datetime = field(default_factory=datetime.utcnow)

    # ==========================================================
    # Step 管理
    # ==========================================================

    def add_step(
        self,
        step: WorkflowStep,
    ) -> None:
        """
        添加 Step
        """

        self.steps.append(step)

        self.updated_at = datetime.utcnow()

    def extend_steps(
        self,
        steps: List[WorkflowStep],
    ) -> None:
        """
        批量添加 Step
        """

        self.steps.extend(steps)

        self.updated_at = datetime.utcnow()

    def get_step(
        self,
        step_id: str,
    ) -> Optional[WorkflowStep]:
        """
        根据 ID 获取 Step
        """

        for step in self.steps:

            if step.step_id == step_id:
                return step

        return None

    def get_current_step(
        self,
    ) -> Optional[WorkflowStep]:
        """
        当前 Step
        """

        if (
            self.current_step_index < 0
            or
            self.current_step_index >= len(self.steps)
        ):
            return None

        return self.steps[self.current_step_index]

    def next_step(
        self,
    ) -> Optional[WorkflowStep]:
        """
        下一个 Step
        """

        if self.current_step_index + 1 >= len(self.steps):

            return None

        self.current_step_index += 1

        return self.steps[self.current_step_index]

    # ==========================================================
    # Workflow 生命周期
    # ==========================================================

    def start(self):
        """
        Workflow 开始
        """

        self.state = WorkflowState.RUNNING

        self.current_step_index = -1

        self.updated_at = datetime.utcnow()

    def success(self):
        """
        Workflow 成功
        """

        self.state = WorkflowState.SUCCESS

        self.updated_at = datetime.utcnow()

    def fail(self):
        """
        Workflow 失败
        """

        self.state = WorkflowState.FAILED

        self.updated_at = datetime.utcnow()

    def cancel(self):
        """
        Workflow 取消
        """

        self.state = WorkflowState.CANCELLED

        self.updated_at = datetime.utcnow()

    # ==========================================================
    # 判断
    # ==========================================================

    def is_finished(
        self,
    ) -> bool:
        """
        是否结束
        """

        return self.state.is_finished()

    def has_next_step(
        self,
    ) -> bool:
        """
        是否还有 Step
        """

        return self.current_step_index + 1 < len(self.steps)

    def step_count(
        self,
    ) -> int:
        """
        Step 数量
        """

        return len(self.steps)

    # ==========================================================
    # Reset
    # ==========================================================

    def reset(self):
        """
        重置 Workflow
        """

        self.state = WorkflowState.CREATED

        self.current_step_index = -1

        for step in self.steps:
            step.reset()

        if self.context:
            self.context.reset_runtime()

        self.updated_at = datetime.utcnow()

    # ==========================================================
    # Dict
    # ==========================================================

    def to_dict(self) -> Dict[str, Any]:
        """
        序列化
        """

        return {

            "workflow_id": self.workflow_id,

            "name": self.name,

            "description": self.description,

            "state": self.state.value,

            "step_count": len(self.steps),

            "current_step_index": self.current_step_index,

            "created_at": self.created_at.isoformat(),

            "updated_at": self.updated_at.isoformat(),

            "metadata": self.metadata,

            "steps": [
                step.to_dict()
                for step in self.steps
            ],

            "context": (
                self.context.to_dict()
                if self.context
                else None
            )
        }

    # ==========================================================
    # String
    # ==========================================================

    def __str__(self):

        return (
            f"<Workflow("
            f"id={self.workflow_id}, "
            f"name={self.name}, "
            f"state={self.state.value}, "
            f"steps={len(self.steps)})>"
        )

    __repr__ = __str__