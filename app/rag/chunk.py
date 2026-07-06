from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4


@dataclass
class Chunk:
    """
    RAG 文本块（Chunk）

    一个 Document 可以拆分为多个 Chunk。

    Chunk 是：
        - Embedding 的最小单位
        - VectorStore 的存储单位
        - Retriever 的检索单位
    """

    # 唯一ID
    id: str = field(default_factory=lambda: str(uuid4()))

    # 所属Document
    document_id: str = ""

    # 第几个Chunk
    chunk_index: int = 0

    # 文本内容
    content: str = ""

    # 来源
    source: str = ""

    # 标题
    title: str = ""

    # Embedding向量（后续生成）
    embedding: Optional[List[float]] = None

    # 检索得分
    score: float = 0.0

    # 元数据
    metadata: Dict[str, Any] = field(default_factory=dict)

    # 创建时间
    created_at: datetime = field(default_factory=datetime.utcnow)

    # 更新时间
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # ==========================================================
    # Property
    # ==========================================================

    @property
    def length(self) -> int:
        """
        Chunk长度
        """
        return len(self.content)

    @property
    def has_embedding(self) -> bool:
        """
        是否已经生成Embedding
        """
        return self.embedding is not None

    @property
    def is_empty(self) -> bool:
        """
        是否为空
        """
        return not self.content.strip()

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
        default: Any = None,
    ) -> Any:
        return self.metadata.get(key, default)

    def update_metadata(
        self,
        values: Dict[str, Any],
    ) -> None:
        self.metadata.update(values)

    def remove_metadata(
        self,
        key: str,
    ) -> None:
        self.metadata.pop(key, None)

    # ==========================================================
    # Embedding
    # ==========================================================

    def set_embedding(
        self,
        embedding: List[float],
    ) -> None:
        """
        设置Embedding向量
        """
        self.embedding = embedding
        self.touch()

    def clear_embedding(self) -> None:
        """
        清除Embedding
        """
        self.embedding = None
        self.touch()

    # ==========================================================
    # Score
    # ==========================================================

    def update_score(
        self,
        score: float,
    ) -> None:
        """
        更新检索得分
        """
        self.score = score

    # ==========================================================
    # Time
    # ==========================================================

    def touch(self) -> None:
        """
        更新时间
        """
        self.updated_at = datetime.utcnow()

    # ==========================================================
    # Serialization
    # ==========================================================

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "document_id": self.document_id,
            "chunk_index": self.chunk_index,
            "title": self.title,
            "content": self.content,
            "source": self.source,
            "embedding": self.embedding,
            "score": self.score,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ) -> "Chunk":
        return cls(
            id=data.get("id", str(uuid4())),
            document_id=data.get("document_id", ""),
            chunk_index=data.get("chunk_index", 0),
            title=data.get("title", ""),
            content=data.get("content", ""),
            source=data.get("source", ""),
            embedding=data.get("embedding"),
            score=data.get("score", 0.0),
            metadata=data.get("metadata", {}),
            created_at=datetime.fromisoformat(
                data["created_at"]
            ) if data.get("created_at") else datetime.utcnow(),
            updated_at=datetime.fromisoformat(
                data["updated_at"]
            ) if data.get("updated_at") else datetime.utcnow(),
        )

    # ==========================================================
    # Magic Method
    # ==========================================================

    def __len__(self) -> int:
        return self.length

    def __bool__(self) -> bool:
        return not self.is_empty

    def __repr__(self) -> str:
        return (
            f"Chunk("
            f"id='{self.id}', "
            f"document_id='{self.document_id}', "
            f"index={self.chunk_index}, "
            f"length={self.length}, "
            f"score={self.score:.4f}"
            f")"
        )