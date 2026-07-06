"""
Workflow Step

工作流中的一个执行节点。

一个 Workflow 由多个 WorkflowStep 组成，每个 Step 负责完成一个独立任务，例如：

- Tool 调用
- LLM 推理
- Memory 查询
- 条件判断
- 自定义函数

企业级设计：
- 支持依赖关系
- 支持重试
- 支持超时（预留）
- 支持条件执行（预留）
- 支持 Metadata
"""

from __future__ import annotations

import traceback
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from app.agent.workflow.workflow_context import WorkflowContext
from app.agent.workflow.workflow_state import WorkflowState


class StepType(str, Enum):
    """
    Workflow Step 类型
    """

    TOOL = "tool"

    LLM = "llm"

    MEMORY = "memory"

    CONDITION = "condition"

    FUNCTION = "function"

    OUTPUT = "output"


@dataclass
class WorkflowStepResult:
    """
    单个 Step 的执行结果
    """

    step_id: str

    success: bool

    output: Any = None

    error: Optional[str] = None

    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowStep:
    """
    Workflow 中的一个节点
    """

    # ==========================
    # 基础信息
    # ==========================

    step_id: str

    name: str

    step_type: StepType

    # ==========================
    # 执行器
    # ==========================

    executor: Optional[Callable[..., Any]] = None

    # ==========================
    # Tool参数
    # ==========================

    inputs: Dict[str, Any] = field(default_factory=dict)

    outputs: Dict[str, Any] = field(default_factory=dict)

    # ==========================
    # Workflow控制
    # ==========================

    depends_on: List[str] = field(default_factory=list)

    retry: int = 0

    timeout: Optional[int] = None

    condition: Optional[Callable[[WorkflowContext], bool]] = None

    metadata: Dict[str, Any] = field(default_factory=dict)

    # ==========================
    # Runtime
    # ==========================

    state: WorkflowState = WorkflowState.CREATED

    error: Optional[str] = None

    execution_count: int = 0

    # ============================================================
    # 是否可以执行
    # ============================================================

    def can_run(
        self,
        context: WorkflowContext,
    ) -> bool:
        """
        判断当前Step是否满足执行条件
        """

        # 条件节点

        if self.condition is not None:

            return self.condition(context)

        return True

    # ============================================================
    # Execute
    # ============================================================

    def execute(
        self,
        context: WorkflowContext,
    ) -> WorkflowStepResult:
        """
        执行当前Step
        """

        self.execution_count += 1

        self.state = WorkflowState.RUNNING

        context.current_step = self.step_id

        try:

            if not self.can_run(context):

                self.state = WorkflowState.SUCCESS

                return WorkflowStepResult(
                    step_id=self.step_id,
                    success=True,
                    output=None,
                    metadata={
                        "skipped": True
                    }
                )

            if self.executor is None:

                raise RuntimeError(
                    f"{self.name} executor is None"
                )

            # executor统一接收context和inputs
            result = self.executor(
                context=context,
                **self.inputs
            )

            self.outputs["result"] = result

            context.shared_data[self.step_id] = result

            context.mark_step_completed(
                self.step_id
            )

            self.state = WorkflowState.SUCCESS

            return WorkflowStepResult(
                step_id=self.step_id,
                success=True,
                output=result,
            )

        except Exception as e:

            self.error = str(e)

            self.state = WorkflowState.FAILED

            context.mark_step_failed(
                self.step_id
            )

            context.add_log(
                traceback.format_exc()
            )

            return WorkflowStepResult(
                step_id=self.step_id,
                success=False,
                error=str(e),
            )

    # ============================================================
    # Retry
    # ============================================================

    def should_retry(self) -> bool:
        """
        是否需要重试
        """

        return (
            self.state == WorkflowState.FAILED
            and self.execution_count <= self.retry
        )

    # ============================================================
    # Reset
    # ============================================================

    def reset(self):
        """
        重置运行状态
        """

        self.state = WorkflowState.CREATED

        self.error = None

        self.outputs.clear()

        self.execution_count = 0

    # ============================================================
    # Dict
    # ============================================================

    def to_dict(self) -> Dict[str, Any]:

        return {

            "step_id": self.step_id,

            "name": self.name,

            "type": self.step_type.value,

            "state": self.state.value,

            "depends_on": self.depends_on,

            "retry": self.retry,

            "timeout": self.timeout,

            "inputs": self.inputs,

            "outputs": self.outputs,

            "metadata": self.metadata,
        }

    # ============================================================
    # String
    # ============================================================

    def __str__(self):

        return (
            f"<WorkflowStep("
            f"id={self.step_id}, "
            f"name={self.name}, "
            f"type={self.step_type.value}, "
            f"state={self.state.value})>"
        )

    __repr__ = __str__