from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from app.rag.document import Document
from app.rag.chunk import Chunk

from app.rag.loaders.loader_manager import LoaderManager
from app.rag.splitters.base_splitter import BaseSplitter
from app.rag.embedding.embedding_manager import EmbeddingManager
from app.rag.vectorstore.vector_store_manager import VectorStoreManager


class KnowledgeBase:

    def __init__(
        self,
        loader_manager: LoaderManager,
        splitter: BaseSplitter,
        embedding_manager: EmbeddingManager,
        vector_store_manager: VectorStoreManager,
        embedding_model: Optional[str] = None,
        vector_store: Optional[str] = None,
    ):

        self.loader_manager = loader_manager

        self.splitter = splitter

        self.embedding_manager = embedding_manager

        self.vector_store_manager = vector_store_manager

        self.embedding_model = embedding_model

        self.vector_store = vector_store