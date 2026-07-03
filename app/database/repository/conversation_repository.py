from typing import Dict, List, Optional
from app.conversation.conversation import Conversation


class ConversationRepository:
    """
    会话存储（内存版 / 可替换DB）
    """

    def __init__(self):
        # key: conversation_id
        self.store: Dict[str, Conversation] = {}

    def create(self, conversation: Conversation):

        self.store[conversation.id] = conversation
        return conversation

    def get(self, conversation_id: str) -> Optional[Conversation]:

        return self.store.get(conversation_id)

    def list_by_user(self, user_id: str) -> List[Conversation]:

        return [
            c for c in self.store.values()
            if c.user_id == user_id
        ]

    def update(self, conversation: Conversation):

        self.store[conversation.id] = conversation