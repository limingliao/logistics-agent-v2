from __future__ import annotations

from typing import Dict

from rag.embedding.base_embedding import BaseEmbedding


class EmbeddingManager:
    """
    Embedding管理器
    """

    def __init__(self):

        self._embeddings: Dict[str, BaseEmbedding] = {}

        self._default = None

    def register(
        self,
        embedding: BaseEmbedding,
        default: bool = False,
    ):

        self._embeddings[
            embedding.model_name
        ] = embedding

        if default or self._default is None:
            self._default = embedding.model_name

    def get(
        self,
        model_name: str = None,
    ) -> BaseEmbedding:

        if model_name is None:
            model_name = self._default

        if model_name not in self._embeddings:
            raise ValueError(
                f"Embedding [{model_name}] not found."
            )

        return self._embeddings[model_name]

    def embed_query(
        self,
        text: str,
        model_name: str = None,
    ):

        return self.get(model_name).embed_query(text)

    def embed_documents(
        self,
        texts,
        model_name=None,
    ):

        return self.get(
            model_name
        ).embed_documents(texts)

    def models(self):

        return list(self._embeddings.keys())