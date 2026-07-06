from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from rag.document import Document


class BaseLoader(ABC):
    """
    文档加载器抽象基类

    Loader负责：

        File
            ↓
        Document

    所有Loader都应继承该类。
    """

    def __init__(
        self,
        encoding: str = "utf-8",
    ):
        self.encoding = encoding

    # ==========================================================
    # Property
    # ==========================================================

    @property
    @abstractmethod
    def loader_name(self) -> str:
        """
        Loader名称
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def supported_extensions(self) -> List[str]:
        """
        支持的文件扩展名
        """
        raise NotImplementedError

    # ==========================================================
    # Load
    # ==========================================================

    @abstractmethod
    def load(
        self,
        file_path: str,
    ) -> Document:
        """
        加载单个文件
        """
        raise NotImplementedError

    def load_many(
        self,
        file_paths: List[str],
    ) -> List[Document]:
        """
        批量加载文件
        """
        return [
            self.load(path)
            for path in file_paths
        ]

    # ==========================================================
    # Validation
    # ==========================================================

    def exists(
        self,
        file_path: str,
    ) -> bool:
        """
        文件是否存在
        """
        return Path(file_path).exists()

    def validate(
        self,
        file_path: str,
    ) -> None:
        """
        校验文件是否合法
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        if not path.is_file():
            raise ValueError(
                f"Not a file: {file_path}"
            )

        ext = path.suffix.lower()

        if ext not in self.supported_extensions:
            raise ValueError(
                f"Unsupported file type: {ext}"
            )

    # ==========================================================
    # Helper
    # ==========================================================

    def create_document(
        self,
        file_path: str,
        content: str,
    ) -> Document:
        """
        创建Document对象
        """
        path = Path(file_path)

        return Document(
            title=path.stem,
            content=content,
            source=str(path),
            doc_type=path.suffix.lower().lstrip("."),
            metadata={
                "file_name": path.name,
                "file_size": path.stat().st_size,
                "extension": path.suffix.lower(),
            },
        )

    # ==========================================================
    # Magic Method
    # ==========================================================

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name='{self.loader_name}')"
        )