from typing import List, Dict, Any

from app.memory.memory_repository import MemoryRepository


class MemoryService:

    def __init__(self, repo: MemoryRepository):
        self.repo = repo

    def add_message(self, session_id: str, role: str, content: str):

        self.repo.add(session_id, role, content)

    def get_history(self, session_id: str, limit: int = 10) -> List[Dict[str, Any]]:

        records = self.repo.get_recent(session_id, limit)

        return [
            {
                "role": r.role,
                "content": r.content
            }
            for r in reversed(records)
        ]

    def clear_history(self, session_id: str):

        self.repo.clear(session_id)