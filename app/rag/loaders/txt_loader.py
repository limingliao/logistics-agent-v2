from __future__ import annotations

from pathlib import Path

from rag.document import Document
from rag.loaders.base_loader import BaseLoader


class TxtLoader(BaseLoader):
    """
    TXT 文档加载器

    负责：

        TXT File
            ↓
        Document
    """

    @property
    def loader_name(self) -> str:
        return "txt"

    @property
    def supported_extensions(self) -> list[str]:
        return [".txt"]

    # ==========================================================
    # Load
    # ==========================================================

    def load(
        self,
        file_path: str,
    ) -> Document:
        """
        加载 TXT 文件
        """

        self.validate(file_path)

        path = Path(file_path)

        with open(
            path,
            "r",
            encoding=self.encoding,
        ) as f:
            content = f.read()

        document = self.create_document(
            file_path=file_path,
            content=content,
        )

        document.set_metadata(
            "loader",
            self.loader_name,
        )

        document.set_metadata(
            "line_count",
            content.count("\n") + 1 if content else 0,
        )

        document.set_metadata(
            "character_count",
            len(content),
        )

        return document