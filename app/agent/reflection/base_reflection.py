from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ReflectionResult:
    """
    Reflection结果
    """

    passed: bool

    score: int

    retry: bool

    reason: str


class BaseReflection(ABC):
    """
    Reflection抽象基类
    """

    @abstractmethod
    def check(self, answer: str) -> ReflectionResult:
        """
        检查LLM回答
        """
        pass