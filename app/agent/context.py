"""
Agent Context

统一 Agent 生命周期的数据载体（State Object）

替代：
    dict 乱传结构
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# =====================================================
# Plan Step（可选扩展）
# =====================================================

@dataclass
class PlanStep:
    """
    单个执行步骤
    """

    tool: Optional[str]
    args: Dict[str, Any] = field(default_factory=dict)


# =====================================================
# Execution Result
# =====================================================

@dataclass
class ExecutionItem:
    """
    单个工具执行结果
    """

    tool: str
    input: Dict[str, Any] = field(default_factory=dict)
    output: Any = None
    error: Optional[str] = None


# =====================================================
# Agent Context（核心）
# =====================================================

@dataclass
class AgentContext:
    """
    Agent 全生命周期状态对象
    """

    # =========================
    # Input
    # =========================
    message: str

    # =========================
    # Router
    # =========================
    intent: Optional[str] = None
    confidence: float = 0.0
    entities: Dict[str, Any] = field(default_factory=dict)
    # =========================
    # Reasoning
    # =========================

    reasoning_result: Optional[Any] = None
    # =========================
    # Planner
    # =========================
    plan: List[PlanStep] = field(default_factory=list)

    # =========================
    # Executor
    # =========================
    execution_results: List[ExecutionItem] = field(default_factory=list)

    # =========================
    # Response
    # =========================
    response: Optional[str] = None

    # =========================
    # Metadata（未来扩展）
    # =========================
    conversation_id: Optional[str] = None
    user_id: Optional[str] = None

    metadata: Dict[str, Any] = field(default_factory=dict)

    # =========================
    # Memory（预留）
    # =========================
    history: List[Dict[str, Any]] = field(default_factory=list)

    # =========================
    # Debug / Trace
    # =========================
    trace: List[str] = field(default_factory=list)

    def add_trace(self, step: str):
        """
        记录执行路径（用于调试）
        """
        self.trace.append(step)