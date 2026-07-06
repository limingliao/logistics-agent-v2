from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from rag.chunk import Chunk
from rag.document import Document


class BaseSplitter(ABC):
    """
    文本切分器抽象基类

    Splitter 负责：

        Document
            ↓
        Chunk

    所有切分器都应继承该类。
    """

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ):
        """
        Args:
            chunk_size:
                每个 Chunk 的最大字符数

            chunk_overlap:
                相邻 Chunk 的重叠字符数
        """
        if chunk_size <= 0:
            raise ValueError(
                "chunk_size must be greater than 0."
            )

        if chunk_overlap < 0:
            raise ValueError(
                "chunk_overlap cannot be negative."
            )

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size."
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    # ==========================================================
    # Property
    # ==========================================================

    @property
    @abstractmethod
    def splitter_name(self) -> str:
        """
        Splitter名称
        """
        raise NotImplementedError

    # ==========================================================
    # Split
    # ==========================================================

    @abstractmethod
    def split(
        self,
        document: Document,
    ) -> List[Chunk]:
        """
        将 Document 切分为多个 Chunk
        """
        raise NotImplementedError

    @abstractmethod
    def split_text(
        self,
        text: str,
    ) -> List[str]:
        """
        仅切分文本
        """
        raise NotImplementedError

    # ==========================================================
    # Helper
    # ==========================================================

    def create_chunk(
        self,
        document: Document,
        content: str,
        index: int,
    ) -> Chunk:
        """
        根据 Document 创建 Chunk
        """

        metadata = dict(document.metadata)
        metadata["chunk_index"] = index

        return Chunk(
            document_id=document.id,
            chunk_index=index,
            title=document.title,
            source=document.source,
            content=content,
            metadata=metadata,
        )

    # ==========================================================
    # Magic Method
    # ==========================================================

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name='{self.splitter_name}', "
            f"chunk_size={self.chunk_size}, "
            f"chunk_overlap={self.chunk_overlap})"
        )