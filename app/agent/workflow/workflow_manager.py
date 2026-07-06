from __future__ import annotations

from typing import Dict, List, Optional

from app.agent.workflow.workflow import Workflow
from app.agent.workflow.workflow_context import WorkflowContext
from app.agent.workflow.workflow_engine import WorkflowEngine
from app.agent.workflow.workflow_result import WorkflowResult


class WorkflowManager:
    """
    Workflow管理器

    职责：
        - Workflow注册
        - Workflow查询
        - Workflow删除
        - Workflow执行
        - Executor注册代理
    """

    def __init__(
        self,
        tool_dispatcher=None,
        reasoning_engine=None,
        memory_manager=None,
    ):
        self._workflows: Dict[str, Workflow] = {}

        self.engine = WorkflowEngine(
            tool_dispatcher=tool_dispatcher,
            reasoning_engine=reasoning_engine,
            memory_manager=memory_manager,
        )

    # ==========================================================
    # Workflow 管理
    # ==========================================================

    def register(self, workflow: Workflow) -> Workflow:
        """
        注册Workflow
        """
        if workflow.name in self._workflows:
            raise ValueError(
                f"Workflow [{workflow.name}] already exists."
            )

        self._workflows[workflow.name] = workflow
        return workflow

    def unregister(self, workflow_name: str) -> None:
        """
        删除Workflow
        """
        self._workflows.pop(workflow_name, None)

    def clear(self) -> None:
        """
        清空Workflow
        """
        self._workflows.clear()

    # ==========================================================
    # 查询
    # ==========================================================

    def exists(self, workflow_name: str) -> bool:
        """
        Workflow是否存在
        """
        return workflow_name in self._workflows

    def get(self, workflow_name: str) -> Workflow:
        """
        获取Workflow
        """
        workflow = self._workflows.get(workflow_name)

        if workflow is None:
            raise KeyError(
                f"Workflow [{workflow_name}] not found."
            )

        return workflow

    def list(self) -> List[str]:
        """
        获取Workflow名称列表
        """
        return list(self._workflows.keys())

    def all(self) -> List[Workflow]:
        """
        获取所有Workflow对象
        """
        return list(self._workflows.values())

    # ==========================================================
    # 执行
    # ==========================================================

    def execute(
        self,
        workflow: Workflow,
        context: Optional[WorkflowContext] = None,
    ) -> WorkflowResult:
        """
        执行Workflow对象
        """
        return self.engine.execute(
            workflow=workflow,
            context=context,
        )

    def execute_by_name(
        self,
        workflow_name: str,
        context: Optional[WorkflowContext] = None,
    ) -> WorkflowResult:
        """
        根据名称执行Workflow
        """
        workflow = self.get(workflow_name)

        return self.execute(
            workflow=workflow,
            context=context,
        )

    # ==========================================================
    # Executor
    # ==========================================================

    def register_executor(
        self,
        step_type: str,
        executor,
    ) -> None:
        """
        注册新的Executor
        """
        self.engine.register_executor(
            step_type=step_type,
            executor=executor,
        )

    # ==========================================================
    # Magic Methods
    # ==========================================================

    def __contains__(self, workflow_name: str) -> bool:
        return self.exists(workflow_name)

    def __len__(self) -> int:
        return len(self._workflows)

    def __iter__(self):
        return iter(self._workflows.values())

    def __repr__(self) -> str:
        return (
            f"WorkflowManager("
            f"workflows={len(self)}, "
            f"engine={self.engine.__class__.__name__}"
            f")"
        )