from __future__ import annotations

import time
from typing import List, Union

import numpy as np
from sentence_transformers import SentenceTransformer

from app.rag.embedding.base_embedding import BaseEmbedding
from app.rag.embedding.embedding_result import EmbeddingResult


class SentenceTransformerEmbedding(BaseEmbedding):
    """
    Sentence Transformer Embedding 实现


    支持：

        text
          ↓
        SentenceTransformer
          ↓
        vector


    默认推荐中文模型：

        BAAI/bge-small-zh-v1.5

    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-small-zh-v1.5",
        device: str | None = None,
        normalize_embeddings: bool = True,
    ):

        self.model_name = model_name

        self.device = device

        self.normalize_embeddings = normalize_embeddings


        self.model = SentenceTransformer(
            model_name,
            device=device,
        )


    # ==========================================================
    # Properties
    # ==========================================================

    @property
    def embedding_name(self) -> str:

        return "sentence_transformer"


    @property
    def dimension(self) -> int:

        return self.model.get_sentence_embedding_dimension()


    # ==========================================================
    # Embed Single
    # ==========================================================

    def embed(
        self,
        text: str,
    ) -> EmbeddingResult:
        """
        单文本向量化
        """

        start = time.perf_counter()


        vector = self.model.encode(
            text,
            normalize_embeddings=self.normalize_embeddings,
        )


        vector = vector.tolist()


        elapsed = (
            time.perf_counter()
            -
            start
        )


        return EmbeddingResult(
            text=text,
            embedding=vector,
            dimension=len(vector),
            elapsed=elapsed,
            metadata={
                "model": self.model_name,
                "provider": "sentence-transformer",
            },
        )


    # ==========================================================
    # Embed Documents
    # ==========================================================

    def embed_documents(
        self,
        texts: List[str],
    ) -> List[EmbeddingResult]:
        """
        批量Embedding
        """

        start = time.perf_counter()


        vectors = self.model.encode(
            texts,
            normalize_embeddings=self.normalize_embeddings,
        )


        elapsed = (
            time.perf_counter()
            -
            start
        )


        results = []


        for text, vector in zip(
            texts,
            vectors,
        ):

            results.append(
                EmbeddingResult(
                    text=text,
                    embedding=vector.tolist(),
                    dimension=len(vector),
                    elapsed=elapsed / len(texts),
                    metadata={
                        "model": self.model_name,
                        "provider": "sentence-transformer",
                    },
                )
            )


        return results


    # ==========================================================
    # Similarity
    # ==========================================================

    def similarity(
        self,
        a: List[float],
        b: List[float],
    ) -> float:
        """
        计算余弦相似度
        """

        a = np.array(a)

        b = np.array(b)


        score = (
            np.dot(a, b)
            /
            (
                np.linalg.norm(a)
                *
                np.linalg.norm(b)
            )
        )


        return float(score)


    # ==========================================================
    # Health
    # ==========================================================

    def health_check(self):

        try:

            vector = self.model.encode(
                "hello"
            )


            return {
                "status": "ok",
                "dimension": len(vector),
                "model": self.model_name,
            }


        except Exception as e:

            return {
                "status": "error",
                "message": str(e),
            }


    # ==========================================================
    # Magic
    # ==========================================================

    def __repr__(self):

        return (
            f"SentenceTransformerEmbedding("
            f"model='{self.model_name}', "
            f"dimension={self.dimension})"
        )