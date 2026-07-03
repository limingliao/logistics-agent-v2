from typing import List, Dict, Any

from app.memory.base_memory import BaseMemory
from app.memory.memory_service import MemoryService


class ConversationMemory(BaseMemory):

    def __init__(self, service: MemoryService):

        self.service = service

    def load(self, session_id: str, limit: int = 10) -> List[Dict[str, Any]]:

        return self.service.get_history(session_id, limit)

    def save(self, session_id: str, message: Dict[str, Any]) -> None:

        self.service.add_message(
            session_id=session_id,
            role=message["role"],
            content=message["content"]
        )

    def clear(self, session_id: str) -> None:

        self.service.clear_history(session_id)