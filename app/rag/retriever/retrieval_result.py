from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from rag.chunk import Chunk


@dataclass
class RetrievalResult:
    """
    RAG 检索结果

    一个 RetrievalResult 表示一次完整的检索过程。

    包含：
        - 查询内容
        - 检索结果
        - 检索耗时
        - Retriever名称
        - TopK
        - Metadata
    """

    # 原始Query
    query: str

    # 检索到的Chunk
    chunks: List[Chunk] = field(default_factory=list)

    # Retriever名称
    retriever_name: str = ""

    # 检索数量
    top_k: int = 5

    # 总命中数量
    total_hits: int = 0

    # 检索耗时（秒）
    elapsed: float = 0.0

    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    # ==========================================================
    # Property
    # ==========================================================

    @property
    def success(self) -> bool:
        """
        是否成功命中
        """
        return len(self.chunks) > 0

    @property
    def is_empty(self) -> bool:
        """
        是否为空结果
        """
        return len(self.chunks) == 0

    @property
    def count(self) -> int:
        """
        返回Chunk数量
        """
        return len(self.chunks)

    @property
    def scores(self) -> List[float]:
        """
        返回所有Chunk Score
        """
        return [
            chunk.score
            for chunk in self.chunks
        ]

    # ==========================================================
    # Chunk
    # ==========================================================

    def first(self) -> Chunk | None:
        """
        第一条结果
        """
        if self.is_empty:
            return None

        return self.chunks[0]

    def add_chunk(
        self,
        chunk: Chunk,
    ) -> None:
        """
        添加Chunk
        """
        self.chunks.append(chunk)

    def extend(
        self,
        chunks: List[Chunk],
    ) -> None:
        """
        添加多个Chunk
        """
        self.chunks.extend(chunks)

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
            "retriever_name": self.retriever_name,
            "top_k": self.top_k,
            "total_hits": self.total_hits,
            "elapsed": self.elapsed,
            "success": self.success,
            "chunks": [
                chunk.to_dict()
                for chunk in self.chunks
            ],
            "metadata": self.metadata,
        }

    # ==========================================================
    # Magic Method
    # ==========================================================

    def __len__(self) -> int:
        return self.count

    def __bool__(self) -> bool:
        return self.success

    def __repr__(self) -> str:
        return (
            f"RetrievalResult("
            f"query='{self.query}', "
            f"chunks={self.count}, "
            f"hits={self.total_hits}, "
            f"elapsed={self.elapsed:.4f}s)"
        )