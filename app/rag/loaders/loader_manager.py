from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

from app.rag.loaders.base_loader import BaseLoader


class LoaderManager:
    """
    文档加载器管理器

    职责：

        - 注册 loaders
        - 获取 loaders
        - 根据扩展名查找 loaders
        - 自动加载文件
        - 管理默认 loaders
    """

    def __init__(self):

        self._loaders: Dict[str, BaseLoader] = {}

        self._extension_mapping: Dict[str, str] = {}

        self._default_loader: Optional[str] = None

    # ==========================================================
    # Register
    # ==========================================================

    def register(
        self,
        loader: BaseLoader,
        default: bool = False,
    ) -> BaseLoader:

        name = loader.loader_name

        self._loaders[name] = loader

        for ext in loader.supported_extensions:
            self._extension_mapping[
                ext.lower()
            ] = name

        if default or self._default_loader is None:
            self._default_loader = name

        return loader

    # ==========================================================
    # Get
    # ==========================================================

    def get(
        self,
        loader_name: Optional[str] = None,
    ) -> BaseLoader:

        if loader_name is None:
            loader_name = self._default_loader

        if loader_name is None:
            raise RuntimeError(
                "No loaders has been registered."
            )

        if loader_name not in self._loaders:
            raise KeyError(
                f"loaders [{loader_name}] not found."
            )

        return self._loaders[loader_name]

    # ==========================================================
    # Extension
    # ==========================================================

    def get_by_extension(
        self,
        extension: str,
    ) -> BaseLoader:

        extension = extension.lower()

        if not extension.startswith("."):
            extension = "." + extension

        loader_name = self._extension_mapping.get(
            extension
        )

        if loader_name is None:
            raise KeyError(
                f"No loader registered for '{extension}'."
            )

        return self._loaders[loader_name]

    # ==========================================================
    # Load
    # ==========================================================

    def load(
        self,
        file_path: str,
    ):
        """
        自动选择 loaders 加载文件
        """

        suffix = Path(file_path).suffix.lower()

        loader = self.get_by_extension(
            suffix
        )

        return loader.load(file_path)

    def load_many(
        self,
        file_paths: List[str],
    ):
        """
        批量加载文件
        """

        return [
            self.load(path)
            for path in file_paths
        ]

    # ==========================================================
    # Remove
    # ==========================================================

    def remove(
        self,
        loader_name: str,
    ) -> None:

        loader = self._loaders.pop(
            loader_name,
            None,
        )

        if loader is None:
            return

        for ext in loader.supported_extensions:

            self._extension_mapping.pop(
                ext.lower(),
                None,
            )

        if self._default_loader == loader_name:

            self._default_loader = next(
                iter(self._loaders),
                None,
            )

    def clear(self) -> None:

        self._loaders.clear()

        self._extension_mapping.clear()

        self._default_loader = None

    # ==========================================================
    # Query
    # ==========================================================

    def exists(
        self,
        loader_name: str,
    ) -> bool:

        return loader_name in self._loaders

    def names(self) -> List[str]:

        return list(self._loaders.keys())

    def extensions(self) -> List[str]:

        return sorted(
            self._extension_mapping.keys()
        )

    def all(self) -> List[BaseLoader]:

        return list(
            self._loaders.values()
        )

    def count(self) -> int:

        return len(
            self._loaders
        )

    # ==========================================================
    # Default
    # ==========================================================

    def set_default(
        self,
        loader_name: str,
    ) -> None:

        if loader_name not in self._loaders:
            raise KeyError(
                f"loaders [{loader_name}] not found."
            )

        self._default_loader = loader_name

    @property
    def default_loader(self):

        if self._default_loader is None:
            return None

        return self._loaders[
            self._default_loader
        ]

    @property
    def default_loader_name(self):

        return self._default_loader

    # ==========================================================
    # Health
    # ==========================================================

    def health_check(self):

        result = {}

        for name, loader in self._loaders.items():

            try:

                result[name] = True

            except Exception:

                result[name] = False

        return result

    # ==========================================================
    # Magic
    # ==========================================================

    def __contains__(
        self,
        loader_name: str,
    ):

        return self.exists(loader_name)

    def __len__(self):

        return len(self._loaders)

    def __iter__(self):

        return iter(
            self._loaders.values()
        )

    def __repr__(self):

        return (
            f"LoaderManager("
            f"loaders={len(self)}, "
            f"extensions={len(self._extension_mapping)})"
        )