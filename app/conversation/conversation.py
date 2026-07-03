from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Conversation:
    """
    会话实体
    """

    id: str
    user_id: str

    title: Optional[str] = None

    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    is_active: bool = True