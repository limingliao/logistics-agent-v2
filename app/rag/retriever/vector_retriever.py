from __future__ import annotations

import time
from typing import List, Optional

from rag.embedding.embedding_manager import EmbeddingManager
from rag.retriever.base_retriever import BaseRetriever
from rag.retriever.retrieval_result import RetrievalResult
from rag.vectorstore.vector_store_manager import VectorStoreManager


class VectorRetriever(BaseRetriever):
    """
    基于向量数据库的Retriever。

    流程：

        Query
            │
            ▼
        EmbeddingManager
            │
            ▼
        Query Embedding
            │
            ▼
        VectorStore
            │
            ▼
        TopK Chunks
    """

    def __init__(
        self,
        embedding_manager: EmbeddingManager,
        vector_store_manager: VectorStoreManager,
        embedding_model: Optional[str] = None,
        vector_store: Optional[str] = None,
    ):

        self.embedding_manager = embedding_manager
        self.vector_store_manager = vector_store_manager

        self.embedding_model = embedding_model
        self.vector_store = vector_store

    # ---------------------------------------------------------

    @property
    def retriever_name(self) -> str:
        return "vector"

    # ---------------------------------------------------------

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> RetrievalResult:

        start = time.perf_counter()

        embedding = self.embedding_manager.embed_query(
            query,
            self.embedding_model,
        )

        result = self.retrieve_by_embedding(
            embedding,
            top_k,
        )

        result.query = query
        result.elapsed = (
            time.perf_counter() - start
        )

        return result

    # ---------------------------------------------------------

    def retrieve_by_embedding(
        self,
        embedding: List[float],
        top_k: int = 5,
    ) -> RetrievalResult:

        store = self.vector_store_manager.get(
            self.vector_store
        )

        chunks = store.search(
            embedding=embedding,
            top_k=top_k,
        )

        return RetrievalResult(
            query="",
            chunks=chunks,
            retriever_name=self.retriever_name,
            top_k=top_k,
            total_hits=len(chunks),
        )

    # ---------------------------------------------------------

    def similarity_search(
        self,
        query: str,
        top_k: int = 5,
    ) -> RetrievalResult:
        return self.retrieve(query, top_k)

    # ---------------------------------------------------------

    def health_check(self) -> bool:

        try:
            self.embedding_manager.get(
                self.embedding_model
            )

            self.vector_store_manager.get(
                self.vector_store
            )

            return True

        except Exception:

            return False