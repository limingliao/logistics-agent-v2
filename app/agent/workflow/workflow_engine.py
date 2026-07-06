from __future__ import annotations

import time
import traceback
from typing import Optional

from app.agent.workflow.workflow import Workflow
from app.agent.workflow.workflow_context import WorkflowContext
from app.agent.workflow.workflow_result import WorkflowResult
from app.agent.workflow.workflow_state import WorkflowState

from app.agent.workflow.executors.executor_registry import ExecutorRegistry
from app.agent.workflow.executors.tool_executor import ToolExecutor
from app.agent.workflow.executors.llm_executor import LLMExecutor
from app.agent.workflow.executors.python_executor import PythonExecutor
from app.agent.workflow.executors.condition_executor import ConditionExecutor
from app.agent.workflow.executors.custom_executor import CustomExecutor


class WorkflowEngine:
    """
    Workflow执行引擎

    负责：

    1. Workflow生命周期管理
    2. Step调度
    3. Context维护
    4. Result收集

    不负责：

    Tool执行
    LLM执行
    Python执行

    上述职责全部交给Executor。
    """

    def __init__(
        self,
        tool_dispatcher=None,
        reasoning_engine=None,
        memory_manager=None,
    ):
        self.tool_dispatcher = tool_dispatcher
        self.reasoning_engine = reasoning_engine
        self.memory_manager = memory_manager

        self.registry = ExecutorRegistry()

        self._register_builtin_executors()

    ##########################################################
    # Register
    ##########################################################

    def _register_builtin_executors(self):

        self.registry.register(
            "tool",
            ToolExecutor(self.tool_dispatcher)
        )

        self.registry.register(
            "llm",
            LLMExecutor(self.reasoning_engine)
        )

        self.registry.register(
            "python",
            PythonExecutor()
        )

        self.registry.register(
            "condition",
            ConditionExecutor()
        )

        self.registry.register(
            "custom",
            CustomExecutor()
        )

    ##########################################################
    # Public
    ##########################################################

    def register_executor(
        self,
        step_type: str,
        executor,
    ):
        """
        动态注册新的Executor
        """

        self.registry.register(
            step_type,
            executor,
        )

    ##########################################################
    # Execute
    ##########################################################

    def execute(
        self,
        workflow: Workflow,
        context: Optional[WorkflowContext] = None,
    ) -> WorkflowResult:

        start = time.time()

        if context is None:
            context = WorkflowContext()

        context.state = WorkflowState.RUNNING

        logs = []

        try:

            for step in workflow.steps:

                logs.append(
                    f"Start Step [{step.name}]"
                )

                executor = self.registry.get(
                    step.step_type
                )

                result = executor.execute(
                    step,
                    context,
                )

                context.set(
                    step.name,
                    result,
                )

                logs.append(
                    f"Finish Step [{step.name}]"
                )

            context.state = WorkflowState.SUCCESS

            end = time.time()

            return WorkflowResult(
                success=True,
                output=context.data,
                context=context,
                logs=logs,
                elapsed=end - start,
            )

        except Exception as e:

            context.state = WorkflowState.FAILED

            logs.append(str(e))

            logs.append(
                traceback.format_exc()
            )

            end = time.time()

            return WorkflowResult(
                success=False,
                output=context.data,
                context=context,
                logs=logs,
                elapsed=end - start,
                error=str(e),
            )