from __future__ import annotations

import re
from pathlib import Path

from rag.document import Document
from rag.loaders.base_loader import BaseLoader


class MarkdownLoader(BaseLoader):
    """
    Markdown 文档加载器

    负责：

        Markdown File
              ↓
          Document
    """

    @property
    def loader_name(self) -> str:
        return "markdown"

    @property
    def supported_extensions(self) -> list[str]:
        return [
            ".md",
            ".markdown",
        ]

    # ==========================================================
    # Load
    # ==========================================================

    def load(
        self,
        file_path: str,
    ) -> Document:

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

        self._fill_metadata(
            document,
            content,
        )

        return document

    # ==========================================================
    # Metadata
    # ==========================================================

    def _fill_metadata(
        self,
        document: Document,
        content: str,
    ) -> None:
        """
        填充 Markdown 元数据
        """

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

        document.set_metadata(
            "word_count",
            len(content.split()),
        )

        document.set_metadata(
            "heading_count",
            self._count_headings(content),
        )

        document.set_metadata(
            "code_block_count",
            self._count_code_blocks(content),
        )

        document.set_metadata(
            "image_count",
            self._count_images(content),
        )

        document.set_metadata(
            "link_count",
            self._count_links(content),
        )

        document.set_metadata(
            "table_count",
            self._count_tables(content),
        )

    # ==========================================================
    # Statistics
    # ==========================================================

    def _count_headings(
        self,
        text: str,
    ) -> int:
        return len(
            re.findall(
                r"^\s{0,3}#{1,6}\s+",
                text,
                flags=re.MULTILINE,
            )
        )

    def _count_code_blocks(
        self,
        text: str,
    ) -> int:
        return len(
            re.findall(
                r"```[\s\S]*?```",
                text,
            )
        )

    def _count_images(
        self,
        text: str,
    ) -> int:
        return len(
            re.findall(
                r"!\[.*?\]\(.*?\)",
                text,
            )
        )

    def _count_links(
        self,
        text: str,
    ) -> int:
        return len(
            re.findall(
                r"(?<!!)\[.*?\]\(.*?\)",
                text,
            )
        )

    def _count_tables(
        self,
        text: str,
    ) -> int:
        """
        简单统计 Markdown 表格（按表头分隔线）
        """
        return len(
            re.findall(
                r"^\|.+\|\s*$\n^\|[\-\:\| ]+\|\s*$",
                text,
                flags=re.MULTILINE,
            )
        )