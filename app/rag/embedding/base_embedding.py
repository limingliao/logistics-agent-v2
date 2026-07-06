from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from rag.embedding.embedding_result import EmbeddingResult


class BaseEmbedding(ABC):
    """
    Embedding抽象基类
    """

    @property
    @abstractmethod
    def model_name(self) -> str:
        ...

    @property
    @abstractmethod
    def dimension(self) -> int:
        ...

    @abstractmethod
    def embed_documents(
        self,
        texts: List[str],
    ) -> EmbeddingResult:
        """
        文档Embedding
        """
        ...

    @abstractmethod
    def embed_query(
        self,
        text: str,
    ) -> List[float]:
        """
        Query Embedding
        """
        ...