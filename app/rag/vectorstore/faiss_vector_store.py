from __future__ import annotations

import os
import pickle
from typing import Dict, List, Optional

import faiss
import numpy as np

from app.rag.chunk import Chunk
from app.rag.vectorstore.base_vector_store import BaseVectorStore


class FaissVectorStore(BaseVectorStore):
    """
    FAISS向量数据库实现


    结构：

        Vector
          |
          |
        FAISS Index

        +

        Metadata Store


    """

    def __init__(
            self,
            dimension: int,
            index_path: Optional[str] = None,
    ):

        self.dimension = dimension

        self.index_path = index_path

        # FAISS索引

        self.index = faiss.IndexFlatIP(
            dimension
        )

        # chunk存储

        self.documents: Dict[
            int,
            Chunk
        ] = {}

        self.counter = 0

    # ======================================================
    # Properties
    # ======================================================

    @property
    def store_name(self):

        return "faiss"

    @property
    def count(self):

        return self.index.ntotal

    # ======================================================
    # Add
    # ======================================================

    def add(
            self,
            vectors: List[List[float]],
            chunks: List[Chunk],
    ):

        if len(vectors) != len(chunks):
            raise ValueError(
                "vectors and chunks size mismatch"
            )

        matrix = np.array(
            vectors,
            dtype="float32"
        )

        self.index.add(
            matrix
        )

        for chunk in chunks:
            self.documents[
                self.counter
            ] = chunk

            self.counter += 1

    # ======================================================
    # Search
    # ======================================================

    def search(
            self,
            query_vector: List[float],
            top_k: int = 5,
    ):

        vector = np.array(
            [
                query_vector
            ],
            dtype="float32"
        )

        scores, indexes = self.index.search(
            vector,
            top_k
        )

        results = []

        for score, idx in zip(
                scores[0],
                indexes[0],
        ):

            if idx == -1:
                continue

            chunk = self.documents.get(
                int(idx)
            )

            if chunk:
                results.append(
                    {
                        "chunk": chunk,
                        "score": float(score)
                    }
                )

        return results

    # ======================================================
    # Delete
    # ======================================================

    def delete(
            self,
            chunk_id: str,
    ):

        remove_ids = []

        for idx, chunk in self.documents.items():

            if chunk.id == chunk_id:
                remove_ids.append(
                    idx
                )

        if remove_ids:

            ids = np.array(
                remove_ids
            )

            self.index.remove_ids(
                ids
            )

            for idx in remove_ids:
                self.documents.pop(
                    idx,
                    None
                )

    # ======================================================
    # Clear
    # ======================================================

    def clear(self):

        self.index = faiss.IndexFlatIP(
            self.dimension
        )

        self.documents.clear()

        self.counter = 0

    # ======================================================
    # Persistence
    # ======================================================

    def save(
            self,
            path: Optional[str] = None,
    ):

        path = (
                path
                or
                self.index_path
        )

        if not path:
            raise ValueError(
                "index path required"
            )

        faiss.write_index(
            self.index,
            path + ".index"
        )

        with open(
                path + ".meta",
                "wb"
        ) as f:
            pickle.dump(
                self.documents,
                f
            )

    def load(
            self,
            path: Optional[str] = None,
    ):

        path = (
                path
                or
                self.index_path
        )

        if not path:
            raise ValueError(
                "index path required"
            )

        self.index = faiss.read_index(
            path + ".index"
        )

        with open(
                path + ".meta",
                "rb"
        ) as f:
            self.documents = pickle.load(
                f
            )

        self.counter = len(
            self.documents
        )

    # ======================================================
    # Health
    # ======================================================

    def health_check(self):

        return {
            "status": "ok",
            "vectors": self.index.ntotal,
            "dimension": self.dimension
        }

    # ======================================================
    # Magic
    # == == == == == == == == == == == == == == == == == == == == == == == == == == ==

    def __len__(self):

        return self.count

    def __repr__(self):

        return (
            f"FaissVectorStore("
            f"dimension={self.dimension}, "
            f"count={self.count})"
        )