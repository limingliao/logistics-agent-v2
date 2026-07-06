"""
Workflow State

定义整个 Workflow 生命周期状态
"""

from enum import Enum


class WorkflowState(str, Enum):
    """Workflow运行状态"""

    CREATED = "created"

    READY = "ready"

    RUNNING = "running"

    WAITING = "waiting"

    PAUSED = "paused"

    SUCCESS = "success"

    FAILED = "failed"

    CANCELLED = "cancelled"

    RETRYING = "retrying"

    TIMEOUT = "timeout"

    def is_finished(self) -> bool:
        """是否已经结束"""

        return self in {
            WorkflowState.SUCCESS,
            WorkflowState.FAILED,
            WorkflowState.CANCELLED,
            WorkflowState.TIMEOUT,
        }

    def is_running(self) -> bool:
        """是否运行中"""

        return self in {
            WorkflowState.RUNNING,
            WorkflowState.RETRYING,
        }

    def can_resume(self) -> bool:
        """是否允许恢复"""

        return self in {
            WorkflowState.PAUSED,
            WorkflowState.WAITING,
        }