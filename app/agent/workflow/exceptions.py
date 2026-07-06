"""
Workflow Exceptions

统一管理Workflow相关异常。
"""


class WorkflowError(Exception):
    """Workflow基础异常"""

    pass


class WorkflowNotFoundError(WorkflowError):
    """Workflow不存在"""

    pass


class WorkflowAlreadyExistsError(WorkflowError):
    """Workflow已存在"""

    pass


class WorkflowExecutionError(WorkflowError):
    """Workflow执行失败"""

    pass


class ExecutorError(WorkflowError):
    """Executor异常"""

    pass


class ExecutorNotFoundError(ExecutorError):
    """Executor不存在"""

    pass


class InvalidWorkflowError(WorkflowError):
    """Workflow定义非法"""

    pass


class InvalidWorkflowStepError(WorkflowError):
    """Workflow Step非法"""

    pass


class WorkflowTimeoutError(WorkflowExecutionError):
    """Workflow执行超时"""

    pass


class WorkflowCancelledError(WorkflowExecutionError):
    """Workflow取消"""

    pass