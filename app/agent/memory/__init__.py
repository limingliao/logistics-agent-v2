from app.agent.planner import Planner
from app.agent.executor import Executor
from app.agent.response_formatter import ResponseFormatter
from app.agent.intent_router import IntentRouter
from sqlalchemy.orm import Session

def __init__(self, db: Session):

    self.db = db

    self.router = IntentRouter()
    self.planner = Planner()
    self.executor = Executor()
    self.response_formatter = ResponseFormatter()

    # =========================
    # Memory 初始化（关键）
    # =========================
    repo = MemoryRepository(db)
    service = MemoryService(repo)
    conversation_memory = ConversationMemory(service)

    self.memory = MemoryManager(conversation_memory)