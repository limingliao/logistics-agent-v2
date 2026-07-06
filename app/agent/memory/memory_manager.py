from typing import List, Dict, Any

from app.conversation.conversation import Conversation


class MemoryManager:

    def __init__(self, memory: Conversation):

        self.memory = memory

    # =========================
    # Load Context
    # =========================

    def load_context(self, session_id: str) -> List[Dict[str, Any]]:

        return self.memory.load(session_id)

    # =========================
    # Save User Message
    # =========================

    def save_user_message(self, session_id: str, message: str):

        self.memory.save(session_id, {
            "role": "user",
            "content": message
        })

    # =========================
    # Save Assistant Message
    # =========================

    def save_assistant_message(self, session_id: str, message: str):

        self.memory.save(session_id, {
            "role": "assistant",
            "content": message
        })

    # =========================
    # Clear Memory
    # =========================

    def clear(self, session_id: str):

        self.memory.clear(session_id)