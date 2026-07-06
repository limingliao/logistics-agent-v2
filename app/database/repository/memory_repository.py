from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.database.models import Memory



class MemoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def add(self, session_id: str, role: str, content: str):

        record = Memory(
            session_id=session_id,
            role=role,
            content=content
        )

        self.db.add(record)
        self.db.commit()

    def get_recent(self, session_id: str, limit: int = 10) -> List[Memory]:

        return (
            self.db.query(Memory)
            .filter(Memory.session_id == session_id)
            .order_by(Memory.id.desc())
            .limit(limit)
            .all()
        )

    def clear(self, session_id: str):

        self.db.query(Memory).filter(
            Memory.session_id == session_id
        ).delete()

        self.db.commit()