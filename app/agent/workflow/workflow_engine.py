from __future__ import annotations

import time
import traceback
from typing import Any, Dict, Optional

from workflow.workflow import Workflow
from workflow.workflow_step import WorkflowStep
from workflow.workflow_context import WorkflowContext
from workflow.workflow_result import WorkflowResult
from workflow.workflow_state import WorkflowState


class WorkflowEngine:
    """
    Workflow执行引擎

    职责：
        - 顺序执行Workflow
        - 管理WorkflowContext
        - 调度Step
        - 收集执行日志
        - 返回WorkflowResult
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

    #######################################################################
    # Public
    #######################################################################

    def execute(
        self,
        workflow: Workflow,
        context: Optional[WorkflowContext] = None,
    ) -> WorkflowResult:

        start_time = time.time()

        if context is None:
            context = WorkflowContext()

        context.state = WorkflowState.RUNNING

        logs = []

        try:

            for step in workflow.steps:

                logs.append(f"Start Step: {step.name}")

                result = self._execute_step(step, context)

                logs.append(f"Finish Step: {step.name}")

                if result is not None:
                    context.set(step.name, result)

            context.state = WorkflowState.SUCCESS

            end = time.time()

            return WorkflowResult(
                success=True,
                output=context.data,
                context=context,
                logs=logs,
                elapsed=end - start_time,
            )

        except Exception as e:

            context.state = WorkflowState.FAILED

            logs.append(str(e))
            logs.append(traceback.format_exc())

            end = time.time()

            return WorkflowResult(
                success=False,
                output=context.data,
                context=context,
                logs=logs,
                elapsed=end - start_time,
                error=str(e),
            )

    #######################################################################
    # Step Dispatcher
    #######################################################################

    def _execute_step(
        self,
        step: WorkflowStep,
        context: WorkflowContext,
    ) -> Any:

        step_type = step.step_type.lower()

        if step_type == "tool":
            return self._execute_tool(step, context)

        elif step_type == "llm":
            return self._execute_llm(step, context)

        elif step_type == "python":
            return self._execute_python(step, context)

        elif step_type == "condition":
            return self._execute_condition(step, context)

        elif step_type == "custom":
            return self._execute_custom(step, context)

        else:
            raise ValueError(f"Unknown step type: {step_type}")

    #######################################################################
    # Tool
    #######################################################################

    def _execute_tool(
        self,
        step: WorkflowStep,
        context: WorkflowContext,
    ):

        if self.tool_dispatcher is None:
            raise RuntimeError("ToolDispatcher not configured.")

        return self.tool_dispatcher.dispatch(
            tool_name=step.action,
            params=step.params,
            context=context,
        )

    #######################################################################
    # LLM
    #######################################################################

    def _execute_llm(
        self,
        step: WorkflowStep,
        context: WorkflowContext,
    ):

        if self.reasoning_engine is None:
            raise RuntimeError("ReasoningEngine not configured.")

        return self.reasoning_engine.reason(
            prompt=step.action,
            context=context,
        )

    #######################################################################
    # Python
    #######################################################################

    def _execute_python(
        self,
        step: WorkflowStep,
        context: WorkflowContext,
    ):

        local_vars = {
            "context": context,
            "result": None,
        }

        exec(step.action, {}, local_vars)

        return local_vars.get("result")

    #######################################################################
    # Condition
    #######################################################################

    def _execute_condition(
        self,
        step: WorkflowStep,
        context: WorkflowContext,
    ):

        condition = step.action

        return eval(condition, {}, {"context": context})

    #######################################################################
    # Custom
    #######################################################################

    def _execute_custom(
        self,
        step: WorkflowStep,
        context: WorkflowContext,
    ):

        if callable(step.action):
            return step.action(context)

        raise RuntimeError("Custom Step must be callable.")