import uuid
from datetime import datetime

from app.conversation.conversation import Conversation
from app.conversation.conversation_repository import ConversationRepository


class ConversationService:

    def __init__(self, repo: ConversationRepository):

        self.repo = repo

    def create_conversation(self, user_id: str) -> Conversation:

        conversation = Conversation(
            id=str(uuid.uuid4()),
            user_id=user_id,
            title="New Chat",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        return self.repo.create(conversation)

    def get_conversation(self, conversation_id: str):

        return self.repo.get(conversation_id)

    def get_or_create(self, user_id: str, conversation_id: str = None):

        if conversation_id:

            conv = self.repo.get(conversation_id)
            if conv:
                return conv

        return self.create_conversation(user_id)