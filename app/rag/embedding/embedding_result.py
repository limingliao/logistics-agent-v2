from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class EmbeddingResult:
    """
    Embedding结果
    """

    vectors: List[List[float]]

    model: str = ""

    dimension: int = 0

    usage: Dict[str, Any] = field(default_factory=dict)

    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def count(self) -> int:
        return len(self.vectors)

    @property
    def is_empty(self) -> bool:
        return self.count == 0

    def first(self) -> List[float]:
        if self.is_empty:
            return []
        return self.vectors[0]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "vectors": self.vectors,
            "model": self.model,
            "dimension": self.dimension,
            "usage": self.usage,
            "metadata": self.metadata,
        }