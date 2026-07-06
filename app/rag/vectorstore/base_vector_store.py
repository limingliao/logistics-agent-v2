from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from rag.chunk import Chunk


class BaseVectorStore(ABC):
    """
    向量数据库抽象基类

    所有向量数据库（FAISS、Chroma、Milvus、PGVector等）
    都应该继承该类。
    """

    @property
    @abstractmethod
    def store_name(self) -> str:
        """
        向量库名称
        """
        raise NotImplementedError

    # ==========================================================
    # CRUD
    # ==========================================================

    @abstractmethod
    def add(self, chunks: List[Chunk]) -> None:
        """
        添加Chunk
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, chunk_ids: List[str]) -> None:
        """
        删除Chunk
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, chunks: List[Chunk]) -> None:
        """
        更新Chunk
        """
        raise NotImplementedError

    @abstractmethod
    def get(self, chunk_id: str) -> Optional[Chunk]:
        """
        获取Chunk
        """
        raise NotImplementedError

    # ==========================================================
    # Search
    # ==========================================================

    @abstractmethod
    def search(
        self,
        embedding: List[float],
        top_k: int = 5,
    ) -> List[Chunk]:
        """
        向量检索
        """
        raise NotImplementedError

    # ==========================================================
    # Collection
    # ==========================================================

    @abstractmethod
    def count(self) -> int:
        """
        Chunk数量
        """
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        """
        清空向量库
        """
        raise NotImplementedError

    # ==========================================================
    # Persistence
    # ==========================================================

    @abstractmethod
    def save(self, path: str) -> None:
        """
        保存向量库
        """
        raise NotImplementedError

    @abstractmethod
    def load(self, path: str) -> None:
        """
        加载向量库
        """
        raise NotImplementedError

    # ==========================================================
    # Magic Methods
    # ==========================================================

    def __len__(self) -> int:
        return self.count()

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name='{self.store_name}', "
            f"count={self.count()})"
        )