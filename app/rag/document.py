from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import uuid4


@dataclass
class Document:
    """
    RAG 文档对象

    一个 Document 表示一份完整文档，例如：

    - PDF
    - Word
    - Markdown
    - TXT
    - HTML
    - FAQ
    - 数据库记录

    后续经过 Splitter 可拆分为多个 Chunk。
    """

    # 唯一ID
    id: str = field(default_factory=lambda: str(uuid4()))

    # 文档标题
    title: str = ""

    # 文档正文
    content: str = ""

    # 来源
    source: str = ""

    # 文档类型
    doc_type: str = "text"

    # 元数据
    metadata: Dict[str, Any] = field(default_factory=dict)

    # 创建时间
    created_at: datetime = field(default_factory=datetime.utcnow)

    # 更新时间
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # ==========================================================
    # 基础属性
    # ==========================================================

    @property
    def length(self) -> int:
        """
        文档长度（字符数）
        """
        return len(self.content)

    @property
    def is_empty(self) -> bool:
        """
        是否为空文档
        """
        return not self.content.strip()

    # ==========================================================
    # Metadata
    # ==========================================================

    def set_metadata(self, key: str, value: Any) -> None:
        """
        设置Metadata
        """
        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Optional[Any] = None,
    ) -> Any:
        """
        获取Metadata
        """
        return self.metadata.get(key, default)

    def update_metadata(
        self,
        values: Dict[str, Any],
    ) -> None:
        """
        批量更新Metadata
        """
        self.metadata.update(values)

    def remove_metadata(self, key: str) -> None:
        """
        删除Metadata
        """
        self.metadata.pop(key, None)

    # ==========================================================
    # Content
    # ==========================================================

    def update_content(self, content: str) -> None:
        """
        更新正文
        """
        self.content = content
        self.touch()

    def append_content(self, text: str) -> None:
        """
        追加正文
        """
        self.content += text
        self.touch()

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
        """
        转换为Dict
        """
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "source": self.source,
            "doc_type": self.doc_type,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ) -> "Document":
        """
        从Dict创建Document
        """
        return cls(
            id=data.get("id", str(uuid4())),
            title=data.get("title", ""),
            content=data.get("content", ""),
            source=data.get("source", ""),
            doc_type=data.get("doc_type", "text"),
            metadata=data.get("metadata", {}),
            created_at=datetime.fromisoformat(
                data["created_at"]
            ) if data.get("created_at") else datetime.utcnow(),
            updated_at=datetime.fromisoformat(
                data["updated_at"]
            ) if data.get("updated_at") else datetime.utcnow(),
        )

    # ==========================================================
    # Magic Methods
    # ==========================================================

    def __len__(self) -> int:
        return self.length

    def __bool__(self) -> bool:
        return not self.is_empty

    def __repr__(self) -> str:
        return (
            f"Document("
            f"id='{self.id}', "
            f"title='{self.title}', "
            f"length={self.length}, "
            f"type='{self.doc_type}'"
            f")"
        )