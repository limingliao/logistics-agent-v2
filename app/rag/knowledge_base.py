from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from rag.document import Document
from rag.chunk import Chunk

from rag.loaders.loader_manager import LoaderManager
from rag.splitters.base_splitter import BaseSplitter
from rag.embedding.embedding_manager import EmbeddingManager
from rag.vectorstore.vector_store_manager import VectorStoreManager


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