from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from app.rag.chunk import Chunk


@dataclass
class RetrievalResult:
    """
    检索结果

    表示一次 Retriever 执行结果：

        Query

          ↓

        Retriever

          ↓

        Chunks + Scores

    """


    # ==========================================
    # Query
    # ==========================================

    query: str


    # ==========================================
    # Retrieved Chunks
    # ==========================================

    chunks: List[Chunk] = field(
        default_factory=list
    )


    # ==========================================
    # Similarity Scores
    # ==========================================

    scores: List[float] = field(
        default_factory=list
    )


    # ==========================================
    # Statistics
    # ==========================================

    elapsed: float = 0.0


    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


    # ==========================================
    # Properties
    # ==========================================

    @property
    def success(self) -> bool:

        return len(self.chunks) > 0


    @property
    def count(self) -> int:

        return len(self.chunks)


    @property
    def top_score(self) -> Optional[float]:
        """
        最高相似度
        """

        if not self.scores:
            return None

        return max(self.scores)



    # ==========================================
    # Get Result
    # ==========================================

    def get(
        self,
        index: int,
    ):

        if index >= len(self.chunks):

            return None


        return {
            "chunk": self.chunks[index],

            "score": (
                self.scores[index]
                if index < len(self.scores)
                else None
            )
        }



    # ==========================================
    # Add
    # ==========================================

    def add(
        self,
        chunk: Chunk,
        score: float = 0.0,
    ):

        self.chunks.append(
            chunk
        )

        self.scores.append(
            score
        )


    # ==========================================
    # Serialization
    # ==========================================

    def to_dict(self):

        return {

            "query": self.query,

            "success": self.success,

            "count": self.count,

            "elapsed": self.elapsed,

            "scores": self.scores,

            "chunks": [

                chunk.to_dict()

                for chunk in self.chunks

            ],

            "metadata": self.metadata,
        }



    # ==========================================
    # Magic
    # ==========================================

    def __len__(self):

        return self.count


    def __bool__(self):

        return self.success


    def __repr__(self):

        return (

            f"RetrievalResult("

            f"query='{self.query}', "

            f"count={self.count}, "

            f"top_score={self.top_score}"

            ")"

        )