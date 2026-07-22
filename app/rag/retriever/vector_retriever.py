from __future__ import annotations

import time
from typing import Optional

from app.rag.retriever.base_retriever import BaseRetriever
from app.rag.retriever.retrieval_result import RetrievalResult

from app.rag.embedding.embedding_manager import EmbeddingManager
from app.rag.vectorstore.vector_store_manager import VectorStoreManager



class VectorRetriever(BaseRetriever):
    """
    向量检索器


    Pipeline:

        Query

          ↓

        Embedding

          ↓

        VectorStore Search

          ↓

        RetrievalResult

    """

    def __init__(
        self,
        embedding_manager: EmbeddingManager,
        vector_store_manager: VectorStoreManager,

        embedding_name: Optional[str] = None,
        vector_store_name: Optional[str] = None,

    ):

        self.embedding_manager = embedding_manager

        self.vector_store_manager = vector_store_manager


        self.embedding_name = embedding_name

        self.vector_store_name = vector_store_name



    # ======================================================
    # Properties
    # ======================================================

    @property
    def retriever_name(self):

        return "vector"



    # ======================================================
    # Retrieve
    # ======================================================

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> RetrievalResult:


        start = time.perf_counter()


        # ---------------------------------
        # 1. 获取 Embedding
        # ---------------------------------

        embedding = (
            self.embedding_manager.get(
                self.embedding_name
            )
        )


        query_embedding = embedding.embed(
            query
        )


        # ---------------------------------
        # 2. 获取 VectorStore
        # ---------------------------------

        vector_store = (
            self.vector_store_manager.get(
                self.vector_store_name
            )
        )


        # ---------------------------------
        # 3. 向量搜索
        # ---------------------------------

        search_results = vector_store.search(
            query_embedding.embedding,
            top_k,
        )


        chunks = []

        scores = []


        for item in search_results:

            chunks.append(
                item["chunk"]
            )

            scores.append(
                item["score"]
            )



        elapsed = (
            time.perf_counter()
            -
            start
        )


        # ---------------------------------
        # 4. 返回 RetrievalResult
        # ---------------------------------

        result = RetrievalResult(

            query=query,

            chunks=chunks,

            scores=scores,

            elapsed=elapsed,

            metadata={

                "retriever": self.retriever_name,

                "embedding":
                    self.embedding_name,

                "vector_store":
                    self.vector_store_name,

                "top_k":
                    top_k,
            }
        )


        return result



    # ======================================================
    # Similarity Search
    # ======================================================

    def similarity_search(
        self,
        query: str,
        top_k: int = 5,
    ):

        return self.retrieve(
            query,
            top_k,
        )



    # ======================================================
    # Health Check
    # ======================================================

    def health_check(self):

        try:

            self.embedding_manager.get(
                self.embedding_name
            )


            self.vector_store_manager.get(
                self.vector_store_name
            )


            return {

                "status":"ok",

                "embedding":
                    self.embedding_name,

                "vector_store":
                    self.vector_store_name
            }


        except Exception as e:

            return {

                "status":"error",

                "message":str(e)
            }



    # ======================================================
    # Magic
    # ======================================================

    def __repr__(self):

        return (

            "VectorRetriever("

            f"embedding={self.embedding_name}, "

            f"vector_store={self.vector_store_name}"

            ")"

        )