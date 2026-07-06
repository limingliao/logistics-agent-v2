"""
Workflow Builder

负责将 ReasoningResult 构建为 Workflow。

WorkflowBuilder 不负责执行 Workflow，
仅负责根据 ReasoningTask 生成 WorkflowStep。
"""

from __future__ import annotations

import uuid
from typing import Optional

from app.agent.reasoning.reasoning_result import (
    ReasoningResult,
    ReasoningTask,
)

from app.agent.workflow.workflow import Workflow
from app.agent.workflow.workflow_context import WorkflowContext
from app.agent.workflow.workflow_step import (
    WorkflowStep,
    StepType,
)

from app.agent.tools.dispatcher import ToolDispatcher


class WorkflowBuilder:
    """
    Workflow 构建器
    """

    def __init__(self):

        pass

    # =====================================================
    # Build
    # =====================================================

    def build(
        self,
        reasoning: ReasoningResult,
        question: str,
        conversation_id: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> Workflow:
        """
        根据 ReasoningResult 构建 Workflow
        """

        workflow_id = str(uuid.uuid4())

        context = WorkflowContext(
            workflow_id=workflow_id,
            question=question,
            conversation_id=conversation_id,
            user_id=user_id,
        )

        context.reasoning_result = reasoning

        workflow = Workflow(
            workflow_id=workflow_id,
            name="Agent Workflow",
            context=context,
        )

        previous_step = None

        # =====================================================
        # Build Tool Steps
        # =====================================================

        for index, task in enumerate(reasoning.tasks):

            step = self._build_step(
                index=index,
                task=task,
            )

            if previous_step is not None:
                step.depends_on.append(
                    previous_step.step_id
                )

            workflow.add_step(step)

            previous_step = step

        # =====================================================
        # Final Output Step
        # =====================================================

        output_step = WorkflowStep(

            step_id="output",

            name="Generate Answer",

            step_type=StepType.OUTPUT,

            executor=self._output_executor,
        )

        if previous_step is not None:
            output_step.depends_on.append(
                previous_step.step_id
            )

        workflow.add_step(output_step)

        return workflow

    # =====================================================
    # Build One Step
    # =====================================================

    def _build_step(
        self,
        index: int,
        task: ReasoningTask,
    ) -> WorkflowStep:

        step_id = f"step_{index + 1}"

        # ----------------------------
        # Tool Step
        # ----------------------------

        if task.tool is not None:

            return WorkflowStep(

                step_id=step_id,

                name=task.name,

                step_type=StepType.TOOL,

                executor=self._tool_executor,

                inputs={

                    "tool_name": task.tool,

                    "tool_args": task.args,
                },
            )

        # ----------------------------
        # LLM Step
        # ----------------------------

        return WorkflowStep(

            step_id=step_id,

            name=task.name,

            step_type=StepType.LLM,

            executor=self._llm_executor,

            inputs={

                "prompt": task.name
            },
        )

    # =====================================================
    # Tool Executor
    # =====================================================

    @staticmethod
    def _tool_executor(
        context: WorkflowContext,
        tool_name: str,
        tool_args: dict,
    ):
        """
        Tool Executor
        """

        result = ToolDispatcher.dispatch(
            tool_name,
            **tool_args
        )

        context.add_tool_result(result)

        return result

    # =====================================================
    # LLM Executor
    # =====================================================

    @staticmethod
    def _llm_executor(
        context: WorkflowContext,
        prompt: str,
    ):
        """
        LLM Step

        当前先占位。

        后续接 DeepSeek / OpenAI
        """

        return {

            "type": "llm",

            "prompt": prompt,
        }

    # =====================================================
    # Output Executor
    # =====================================================

    @staticmethod
    def _output_executor(
        context: WorkflowContext,
    ):
        """
        Workflow 最终输出
        """

        return {

            "answer": context.final_answer,

            "tool_results": context.tool_results,

            "variables": context.variables,
        }