"""
Enterprise Logistics Agent

Agent Orchestrator

职责：

1. Think
2. Intent Routing
3. Planning
4. Execution
"""

from typing import Any, Dict

from sqlalchemy.orm import Session

from app.agent.executor import Executor
from app.agent.intent_router import IntentRouter
from app.agent.planner import Planner
from app.core.exceptions import BusinessException
from app.core.logger import logger

from app.database.repository.conversation_repository import ConversationRepository
from app.services.conversation_service import ConversationService

from app.llm.model import llm
from app.agent.response_formatter import ResponseFormatter
from app.agent.memory.memory_manager import MemoryManager
from app.conversation.conversation import Conversation
from app.services.memory_service import MemoryService
from app.database.repository.memory_repository import MemoryRepository
from app.agent.context import AgentContext
from app.agent.prompts.prompt_manager import PromptManager


class LogisticsAgent:
    """
    企业级 Logistics Agent
    """

    def __init__(self, db: Session):

        self.db = db

        self.router = IntentRouter()

        self.planner = Planner()

        self.executor = Executor()

        self.response_formatter = ResponseFormatter()
        self.conversation_repo = ConversationRepository()
        self.conversation_service = ConversationService(self.conversation_repo)
        # Prompt Manager
        self.prompt_manager = PromptManager()

        # Memory
        memory_repository = MemoryRepository(db)

        memory_service = MemoryService(memory_repository)

        conversation_memory = Conversation(memory_service)

        self.memory = MemoryManager(conversation_memory)

    # =====================================================
    # Chat Entry
    # =====================================================

    def chat(
            self,
            user_id: str,
            message: str,
            conversation_id: str | None = None
    ) -> str:

        if not message:
            raise BusinessException("message不能为空")

        logger.info("=" * 60)
        logger.info("[Agent] Start Chat")
        logger.info(f"[User] {message}")

        try:
            # 先拿conversation
            conversation = self.conversation_service.get_or_create(
                user_id=user_id,
                conversation_id=conversation_id
            )
            # =========================
            # 1. 创建 Context
            # =========================
            context = AgentContext(
                message=message,
                user_id=user_id,
                conversation_id=conversation.id
            )
            # =========================
            # 2. 读取 Memory（关键）
            # =========================
            history = self.memory.load_context(conversation.id)
            context.history = history
            prompt = self.prompt_manager.build(
                user_input=message,
                history=history,
                memory=""
            )
            context.prompt = prompt
            # =========================
            # 3. 路由
            # =========================
            context = self.route(context)
            # =========================
            # 4. 规划
            # =========================
            context = self.plan(context)
            # =========================
            # 5. 执行
            # =========================
            context = self.execute(context)
            context.response = self.chat_with_llm(
                context.prompt
            )
            # =========================
            # 6. 生成回复
            # =========================
            context = self.format(context)
            # =========================
            # 7. 写入 Memory（关键）
            # =========================
            self.memory.save_user_message(conversation.id, message)
            self.memory.save_assistant_message(conversation.id, context.response)

            logger.info("[Agent] Chat Finished")
            return context.response
        except Exception as e:

            logger.exception("[Agent] Chat Failed")

            raise BusinessException("AI服务调用失败") from e

    # =====================================================
    # Think
    # =====================================================

    # def think(
    #     self,
    #     message: str
    # ) -> Dict[str, Any]:
    #
    #     logger.info("[Think]")
    #
    #     return {
    #
    #         "message": message,
    #
    #         "intent": None,
    #
    #         "entities": {}
    #     }
    def think(self, message: str) -> AgentContext:

        return AgentContext(message=message)

    # =====================================================
    # Route
    # =====================================================

    def route(
        self,
        context: AgentContext
    ) -> AgentContext:

        logger.info("[Router]")

        result = self.router.route(
            context.message
        )

        context.intent = result.intent

        context.entities = result.entities

        context.confidence = result.confidence

        return context

    # =====================================================
    # Plan
    # =====================================================

    def plan(
        self,
        context: AgentContext
    ) -> AgentContext:

        logger.info("[Planner]")

        return self.planner.create_plan(context)

    # =====================================================
    # Execute
    # =====================================================

    def execute(
        self,
        context: AgentContext
    ) -> AgentContext:

        logger.info("[Executor]")

        return self.executor.execute(context)


    # =====================================================
    # LLM
    # =====================================================

    def chat_with_llm(
        self,
        message: str
    ) -> str:

        logger.info("[LLM]")

        messages = [
            {

                "role": "user",

                "content": message

            }

        ]

        return llm.chat_with_messages(messages)