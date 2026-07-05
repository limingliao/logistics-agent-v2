"""
Reasoning Data Model

企业级 Reasoning 对象
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ReasoningTask:
    """
    单个推理任务
    """

    name: str

    intent: str

    tool: Optional[str] = None

    args: Dict[str, Any] = field(default_factory=dict)

    depends_on: List[int] = field(default_factory=list)


@dataclass
class ReasoningResult:
    """
    推理结果
    """

    tasks: List[ReasoningTask] = field(default_factory=list)

    reasoning_trace: List[str] = field(default_factory=list)

    success: bool = True

    message: str = ""