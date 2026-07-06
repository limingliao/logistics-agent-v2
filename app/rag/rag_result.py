from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from rag.chunk import Chunk
from rag.retriever.retrieval_result import RetrievalResult


@dataclass
class RAGResult:
    """
    RAG 查询结果

    一个 RAGResult 表示一次完整的 RAG Pipeline。

        Query
            ↓
        Retriever
            ↓
        RetrievalResult
            ↓
        Context Builder
            ↓
        RAGResult
    """

    # ==========================================================
    # Query
    # ==========================================================

    query: str

    # ==========================================================
    # Context
    # ==========================================================

    context: str = ""

    # ==========================================================
    # Retrieved Chunks
    # ==========================================================

    chunks: List[Chunk] = field(default_factory=list)

    # ==========================================================
    # Retrieval Result
    # ==========================================================

    retrieval_result: Optional[RetrievalResult] = None

    # ==========================================================
    # Statistics
    # ==========================================================

    elapsed: float = 0.0

    metadata: Dict[str, Any] = field(default_factory=dict)

    # ==========================================================
    # Properties
    # ==========================================================

    @property
    def success(self) -> bool:
        return len(self.chunks) > 0

    @property
    def count(self) -> int:
        return len(self.chunks)

    @property
    def is_empty(self) -> bool:
        return self.count == 0

    # ==========================================================
    # Chunk Operations
    # ==========================================================

    def add_chunk(
        self,
        chunk: Chunk,
    ) -> None:
        self.chunks.append(chunk)

    def extend(
        self,
        chunks: List[Chunk],
    ) -> None:
        self.chunks.extend(chunks)

    def first(self) -> Optional[Chunk]:
        if self.is_empty:
            return None

        return self.chunks[0]

    # ==========================================================
    # Context
    # ==========================================================

    def set_context(
        self,
        context: str,
    ) -> None:
        self.context = context

    # ==========================================================
    # Metadata
    # ==========================================================

    def set_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default=None,
    ) -> Any:
        return self.metadata.get(key, default)

    # ==========================================================
    # Serialization
    # ==========================================================

    def to_dict(self) -> Dict[str, Any]:

        return {
            "query": self.query,
            "context": self.context,
            "elapsed": self.elapsed,
            "success": self.success,
            "count": self.count,
            "chunks": [
                chunk.to_dict()
                for chunk in self.chunks
            ],
            "metadata": self.metadata,
            "retrieval_result": (
                self.retrieval_result.to_dict()
                if self.retrieval_result
                else None
            ),
        }

    # ==========================================================
    # Magic Methods
    # ==========================================================

    def __len__(self) -> int:
        return self.count

    def __bool__(self) -> bool:
        return self.success

    def __repr__(self) -> str:

        return (
            f"RAGResult("
            f"query='{self.query}', "
            f"chunks={self.count}, "
            f"elapsed={self.elapsed:.4f}s)"
        )