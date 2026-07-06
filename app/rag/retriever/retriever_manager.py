from __future__ import annotations

from typing import Dict, List, Optional

from app.rag.retriever.base_retriever import BaseRetriever


class RetrieverManager:
    """
    Retriever 管理器

    职责：
        - 注册 Retriever
        - 获取 Retriever
        - 管理默认 Retriever
        - 删除 Retriever
    """

    def __init__(self):
        self._retrievers: Dict[str, BaseRetriever] = {}
        self._default_retriever: Optional[str] = None

    # ==========================================================
    # Register
    # ==========================================================

    def register(
        self,
        retriever: BaseRetriever,
        default: bool = False,
    ) -> BaseRetriever:
        """
        注册 Retriever
        """
        self._retrievers[
            retriever.retriever_name
        ] = retriever

        if default or self._default_retriever is None:
            self._default_retriever = (
                retriever.retriever_name
            )

        return retriever

    # ==========================================================
    # Get
    # ==========================================================

    def get(
        self,
        retriever_name: Optional[str] = None,
    ) -> BaseRetriever:
        """
        获取 Retriever
        """
        if retriever_name is None:
            retriever_name = self._default_retriever

        if retriever_name is None:
            raise RuntimeError(
                "No Retriever has been registered."
            )

        if retriever_name not in self._retrievers:
            raise KeyError(
                f"Retriever [{retriever_name}] not found."
            )

        return self._retrievers[retriever_name]

    # ==========================================================
    # Remove
    # ==========================================================

    def remove(
        self,
        retriever_name: str,
    ) -> None:
        """
        删除 Retriever
        """
        self._retrievers.pop(
            retriever_name,
            None,
        )

        if self._default_retriever == retriever_name:
            self._default_retriever = (
                next(
                    iter(self._retrievers),
                    None,
                )
            )

    def clear(self) -> None:
        """
        清空所有 Retriever
        """
        self._retrievers.clear()
        self._default_retriever = None

    # ==========================================================
    # Default
    # ==========================================================

    def set_default(
        self,
        retriever_name: str,
    ) -> None:
        """
        设置默认 Retriever
        """
        if retriever_name not in self._retrievers:
            raise KeyError(
                f"Retriever [{retriever_name}] not found."
            )

        self._default_retriever = retriever_name

    @property
    def default_retriever(self) -> Optional[BaseRetriever]:
        """
        获取默认 Retriever
        """
        if self._default_retriever is None:
            return None

        return self._retrievers[
            self._default_retriever
        ]

    @property
    def default_retriever_name(self) -> Optional[str]:
        """
        获取默认 Retriever 名称
        """
        return self._default_retriever

    # ==========================================================
    # Query
    # ==========================================================

    def exists(
        self,
        retriever_name: str,
    ) -> bool:
        """
        判断 Retriever 是否存在
        """
        return retriever_name in self._retrievers

    def names(self) -> List[str]:
        """
        获取所有 Retriever 名称
        """
        return list(self._retrievers.keys())

    def all(self) -> List[BaseRetriever]:
        """
        获取所有 Retriever
        """
        return list(self._retrievers.values())

    def count(self) -> int:
        """
        获取 Retriever 数量
        """
        return len(self._retrievers)

    # ==========================================================
    # Health
    # ==========================================================

    def health_check(self) -> Dict[str, bool]:
        """
        检查所有 Retriever 状态
        """
        result = {}

        for name, retriever in self._retrievers.items():
            try:
                result[name] = retriever.health_check()
            except Exception:
                result[name] = False

        return result

    # ==========================================================
    # Magic Methods
    # ==========================================================

    def __contains__(
        self,
        retriever_name: str,
    ) -> bool:
        return self.exists(retriever_name)

    def __len__(self) -> int:
        return len(self._retrievers)

    def __iter__(self):
        return iter(self._retrievers.values())

    def __repr__(self) -> str:
        return (
            f"RetrieverManager("
            f"retrievers={len(self)}, "
            f"default='{self._default_retriever}')"
        )