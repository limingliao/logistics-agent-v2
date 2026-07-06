from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from app.rag.chunk import Chunk

from app.rag.retriever.retrieval_result import RetrievalResult


class BaseRetriever(ABC):
    """
    检索器抽象基类

    Retriever负责：

        Question
            ↓
        Embedding
            ↓
        VectorStore
            ↓
        TopK Chunks

    所有Retriever（VectorRetriever、HybridRetriever等）
    都应继承该类。
    """

    @property
    @abstractmethod
    def retriever_name(self) -> str:
        """
        Retriever名称
        """
        raise NotImplementedError

    @abstractmethod
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> RetrievalResult:
        """
        根据Query检索Chunk
        """
        raise NotImplementedError

    @abstractmethod
    def retrieve_by_embedding(
        self,
        embedding: List[float],
        top_k: int = 5,
    ) -> RetrievalResult:
        """
        根据Embedding检索Chunk
        """
        raise NotImplementedError

    @abstractmethod
    def similarity_search(
        self,
        query: str,
        top_k: int = 5,
    ) -> RetrievalResult:
        """
        相似度搜索
        默认与retrieve语义一致，可由具体实现覆盖。
        """
        raise NotImplementedError

    @abstractmethod
    def health_check(self) -> bool:
        """
        检查Retriever是否可用
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(name='{self.retriever_name}')"
        )