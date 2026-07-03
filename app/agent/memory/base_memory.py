from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseMemory(ABC):
    """
    Memory抽象层（所有Memory的标准接口）
    """

    @abstractmethod
    def load(self, session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        加载历史记录
        """
        pass

    @abstractmethod
    def save(self, session_id: str, message: Dict[str, Any]) -> None:
        """
        保存一条记录
        """
        pass

    @abstractmethod
    def clear(self, session_id: str) -> None:
        """
        清空记忆
        """
        pass