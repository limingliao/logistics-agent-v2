"""
Workflow Definition

Workflow 负责维护整个工作流的数据结构，不负责具体执行。

职责：
- 管理 WorkflowStep
- 管理 WorkflowState
- 管理 WorkflowContext
- 提供 Step 查询
- 提供 Workflow 生命周期
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from app.agent.workflow.workflow_context import WorkflowContext
from app.agent.workflow.workflow_state import WorkflowState
from app.agent.workflow.workflow_step import WorkflowStep


@dataclass
class Workflow:
    """
    Workflow 定义
    """

    # ==========================================
    # Basic
    # ==========================================

    workflow_id: str

    name: str

    description: str = ""

    # ==========================================
    # Runtime
    # ==========================================

    context: Optional[WorkflowContext] = None

    state: WorkflowState = WorkflowState.CREATED

    # ==========================================
    # Steps
    # ==========================================

    steps: List[WorkflowStep] = field(default_factory=list)

    current_index: int = 0

    # ==========================================
    # Metadata
    # ==========================================

    metadata: Dict = field(default_factory=dict)

    # =====================================================
    # Add Step
    # =====================================================

    def add_step(
        self,
        step: WorkflowStep,
    ) -> None:

        self.steps.append(step)

    # =====================================================
    # Remove Step
    # =====================================================

    def remove_step(
        self,
        step_id: str,
    ) -> bool:

        for i, step in enumerate(self.steps):

            if step.step_id == step_id:

                self.steps.pop(i)

                return True

        return False

    # =====================================================
    # Get Step
    # =====================================================

    def get_step(
        self,
        step_id: str,
    ) -> Optional[WorkflowStep]:

        for step in self.steps:

            if step.step_id == step_id:

                return step

        return None

    # =====================================================
    # Get Current Step
    # =====================================================

    def current_step(
        self,
    ) -> Optional[WorkflowStep]:

        if self.current_index >= len(self.steps):

            return None

        return self.steps[self.current_index]

    # =====================================================
    # Next Step
    # =====================================================

    def next_step(
        self,
    ) -> Optional[WorkflowStep]:

        self.current_index += 1

        if self.current_index >= len(self.steps):

            return None

        return self.steps[self.current_index]

    # =====================================================
    # Has Next
    # =====================================================

    def has_next(self) -> bool:

        return self.current_index < len(self.steps)

    # =====================================================
    # Total Step
    # =====================================================

    @property
    def total_steps(self):

        return len(self.steps)

    # =====================================================
    # Finished
    # =====================================================

    @property
    def finished(self):

        return self.current_index >= len(self.steps)

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        self.current_index = 0

        self.state = WorkflowState.CREATED

        for step in self.steps:

            step.reset()

        if self.context:

            self.context.reset_runtime()

    # =====================================================
    # Ready
    # =====================================================

    def ready(self):

        self.state = WorkflowState.READY

    # =====================================================
    # Running
    # =====================================================

    def running(self):

        self.state = WorkflowState.RUNNING

    # =====================================================
    # Success
    # =====================================================

    def success(self):

        self.state = WorkflowState.SUCCESS

    # =====================================================
    # Failed
    # =====================================================

    def failed(self):

        self.state = WorkflowState.FAILED

    # =====================================================
    # Pause
    # =====================================================

    def pause(self):

        self.state = WorkflowState.PAUSED

    # =====================================================
    # Resume
    # =====================================================

    def resume(self):

        self.state = WorkflowState.RUNNING

    # =====================================================
    # Validate
    # =====================================================

    def validate(self):

        if self.context is None:

            raise RuntimeError(
                "WorkflowContext is None."
            )

        if len(self.steps) == 0:

            raise RuntimeError(
                "Workflow has no step."
            )

        ids = set()

        for step in self.steps:

            if step.step_id in ids:

                raise RuntimeError(
                    f"Duplicate Step ID: {step.step_id}"
                )

            ids.add(step.step_id)

    # =====================================================
    # Dict
    # =====================================================

    def to_dict(self):

        return {

            "workflow_id": self.workflow_id,

            "name": self.name,

            "description": self.description,

            "state": self.state.value,

            "current_index": self.current_index,

            "total_steps": self.total_steps,

            "metadata": self.metadata,

            "steps": [

                step.to_dict()

                for step in self.steps

            ]
        }

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return (

            f"<Workflow("
            f"id={self.workflow_id}, "
            f"steps={len(self.steps)}, "
            f"state={self.state.value})>"

        )

    __repr__ = __str__