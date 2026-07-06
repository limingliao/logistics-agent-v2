from __future__ import annotations

from typing import Dict, List, Optional

from rag.knowledge_base import KnowledgeBase
from rag.rag_engine import RAGEngine
from rag.rag_result import RAGResult


class RAGManager:
    """
    RAG 管理器

    统一管理：

        - KnowledgeBase
        - RAGEngine

    对外提供统一接口。
    """

    def __init__(self):

        self._knowledge_bases: Dict[str, KnowledgeBase] = {}

        self._engines: Dict[str, RAGEngine] = {}

        self._default_kb: Optional[str] = None

        self._default_engine: Optional[str] = None

    # ==========================================================
    # Knowledge Base
    # ==========================================================

    def register_knowledge_base(
        self,
        name: str,
        kb: KnowledgeBase,
        default: bool = False,
    ) -> KnowledgeBase:

        self._knowledge_bases[name] = kb

        if default or self._default_kb is None:
            self._default_kb = name

        return kb

    def get_knowledge_base(
        self,
        name: Optional[str] = None,
    ) -> KnowledgeBase:

        name = name or self._default_kb

        if name is None:
            raise RuntimeError(
                "No KnowledgeBase registered."
            )

        return self._knowledge_bases[name]

    # ==========================================================
    # Engine
    # ==========================================================

    def register_engine(
        self,
        name: str,
        engine: RAGEngine,
        default: bool = False,
    ) -> RAGEngine:

        self._engines[name] = engine

        if default or self._default_engine is None:
            self._default_engine = name

        return engine

    def get_engine(
        self,
        name: Optional[str] = None,
    ) -> RAGEngine:

        name = name or self._default_engine

        if name is None:
            raise RuntimeError(
                "No RAGEngine registered."
            )

        return self._engines[name]

    # ==========================================================
    # Query
    # ==========================================================

    def query(
        self,
        query: str,
        top_k: int = 5,
        engine: Optional[str] = None,
    ) -> RAGResult:

        rag_engine = self.get_engine(engine)

        return rag_engine.query(
            query=query,
            top_k=top_k,
        )

    # ==========================================================
    # Knowledge Import
    # ==========================================================

    def add_file(
        self,
        file_path: str,
        kb: Optional[str] = None,
    ):

        knowledge_base = self.get_knowledge_base(kb)

        return knowledge_base.add_file(
            file_path
        )

    def add_directory(
        self,
        directory: str,
        recursive: bool = True,
        kb: Optional[str] = None,
    ):

        knowledge_base = self.get_knowledge_base(kb)

        return knowledge_base.add_directory(
            directory,
            recursive,
        )

    # ==========================================================
    # Statistics
    # ==========================================================

    def statistics(self):

        return {
            "knowledge_bases": len(
                self._knowledge_bases
            ),
            "engines": len(
                self._engines
            ),
            "default_kb": self._default_kb,
            "default_engine": self._default_engine,
        }

    # ==========================================================
    # Health
    # ==========================================================

    def health_check(self):

        return {
            name: engine.health_check()
            for name, engine in self._engines.items()
        }

    # ==========================================================
    # Magic Methods
    # ==========================================================

    def __len__(self):

        return len(self._engines)

    def __repr__(self):

        return (
            f"RAGManager("
            f"engines={len(self._engines)}, "
            f"knowledge_bases={len(self._knowledge_bases)})"
        )