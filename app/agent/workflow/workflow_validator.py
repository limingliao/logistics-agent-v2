from __future__ import annotations

from typing import Iterable

from workflow.workflow import Workflow
from workflow.workflow_step import WorkflowStep
from workflow.exceptions import (
    InvalidWorkflowError,
    InvalidWorkflowStepError,
)


class WorkflowValidator:
    """
    Workflow 校验器

    负责：

    - Workflow是否合法
    - Step是否合法
    - Step名称是否重复
    - Workflow是否为空
    """

    DEFAULT_STEP_TYPES = {
        "tool",
        "llm",
        "python",
        "condition",
        "custom",
    }

    @classmethod
    def validate(cls, workflow: Workflow) -> None:

        cls.validate_workflow(workflow)

        cls.validate_steps(workflow.steps)

    # -----------------------------------------------------

    @classmethod
    def validate_workflow(cls, workflow: Workflow):

        if workflow is None:
            raise InvalidWorkflowError(
                "Workflow cannot be None."
            )

        if not workflow.name:
            raise InvalidWorkflowError(
                "Workflow name cannot be empty."
            )

        if not workflow.steps:
            raise InvalidWorkflowError(
                "Workflow must contain at least one step."
            )

    # -----------------------------------------------------

    @classmethod
    def validate_steps(
        cls,
        steps: Iterable[WorkflowStep],
    ):

        names = set()

        for step in steps:

            cls.validate_step(step)

            if step.name in names:
                raise InvalidWorkflowStepError(
                    f"Duplicate step name: {step.name}"
                )

            names.add(step.name)

    # -----------------------------------------------------

    @classmethod
    def validate_step(
        cls,
        step: WorkflowStep,
    ):

        if step is None:
            raise InvalidWorkflowStepError(
                "Step cannot be None."
            )

        if not step.name:
            raise InvalidWorkflowStepError(
                "Step name cannot be empty."
            )

        if not step.step_type:
            raise InvalidWorkflowStepError(
                f"Step [{step.name}] missing step_type."
            )

        if step.step_type.lower() not in cls.DEFAULT_STEP_TYPES:
            raise InvalidWorkflowStepError(
                f"Unsupported step type: {step.step_type}"
            )

        if step.action is None:
            raise InvalidWorkflowStepError(
                f"Step [{step.name}] action cannot be None."
            )