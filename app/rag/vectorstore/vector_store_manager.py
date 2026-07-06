from __future__ import annotations

from typing import Dict, List, Optional

from rag.vectorstore.base_vector_store import BaseVectorStore


class VectorStoreManager:
    """
    向量数据库管理器

    职责：
        - 注册向量数据库
        - 获取向量数据库
        - 管理默认向量数据库
        - 删除向量数据库
    """

    def __init__(self):
        self._stores: Dict[str, BaseVectorStore] = {}
        self._default_store: Optional[str] = None

    # ==========================================================
    # Register
    # ==========================================================

    def register(
        self,
        store: BaseVectorStore,
        default: bool = False,
    ) -> BaseVectorStore:
        """
        注册向量数据库
        """
        self._stores[store.store_name] = store

        if default or self._default_store is None:
            self._default_store = store.store_name

        return store

    # ==========================================================
    # Get
    # ==========================================================

    def get(
        self,
        store_name: Optional[str] = None,
    ) -> BaseVectorStore:
        """
        获取向量数据库
        """
        if store_name is None:
            store_name = self._default_store

        if store_name is None:
            raise RuntimeError(
                "No VectorStore has been registered."
            )

        if store_name not in self._stores:
            raise KeyError(
                f"VectorStore [{store_name}] not found."
            )

        return self._stores[store_name]

    # ==========================================================
    # Remove
    # ==========================================================

    def remove(
        self,
        store_name: str,
    ) -> None:
        """
        删除向量数据库
        """
        self._stores.pop(store_name, None)

        if self._default_store == store_name:
            self._default_store = (
                next(iter(self._stores), None)
            )

    def clear(self) -> None:
        """
        清空所有向量数据库
        """
        self._stores.clear()
        self._default_store = None

    # ==========================================================
    # Default
    # ==========================================================

    def set_default(
        self,
        store_name: str,
    ) -> None:
        """
        设置默认向量数据库
        """
        if store_name not in self._stores:
            raise KeyError(
                f"VectorStore [{store_name}] not found."
            )

        self._default_store = store_name

    @property
    def default_store(self) -> Optional[BaseVectorStore]:
        """
        获取默认向量数据库对象
        """
        if self._default_store is None:
            return None

        return self._stores[self._default_store]

    @property
    def default_store_name(self) -> Optional[str]:
        """
        获取默认向量数据库名称
        """
        return self._default_store

    # ==========================================================
    # Query
    # ==========================================================

    def exists(
        self,
        store_name: str,
    ) -> bool:
        """
        判断向量数据库是否存在
        """
        return store_name in self._stores

    def names(self) -> List[str]:
        """
        获取所有向量数据库名称
        """
        return list(self._stores.keys())

    def all(self) -> List[BaseVectorStore]:
        """
        获取所有向量数据库
        """
        return list(self._stores.values())

    def count(self) -> int:
        """
        获取已注册向量数据库数量
        """
        return len(self._stores)

    # ==========================================================
    # Magic Methods
    # ==========================================================

    def __contains__(self, store_name: str) -> bool:
        return self.exists(store_name)

    def __len__(self) -> int:
        return len(self._stores)

    def __iter__(self):
        return iter(self._stores.values())

    def __repr__(self) -> str:
        return (
            f"VectorStoreManager("
            f"stores={len(self)}, "
            f"default='{self._default_store}')"
        )