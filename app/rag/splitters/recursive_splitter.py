from __future__ import annotations

import re
from typing import List, Optional

from rag.chunk import Chunk
from rag.document import Document
from rag.splitters.base_splitter import BaseSplitter
from rag.splitters.text_splitter import TextSplitter


class RecursiveSplitter(BaseSplitter):
    """
    递归文本切分器

    优先保持语义完整：

        Paragraph
            ↓
        Sentence
            ↓
        Phrase
            ↓
        Word
            ↓
        Character
    """

    DEFAULT_SEPARATORS = [
        "\n\n",
        "\n",
        r"(?<=[。！？])",
        r"(?<=[.!?])",
        r"(?<=[，；：,;:])",
        " ",
    ]

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        separators: Optional[List[str]] = None,
    ):
        super().__init__(chunk_size, chunk_overlap)

        self.separators = separators or self.DEFAULT_SEPARATORS

        self._fallback = TextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    @property
    def splitter_name(self) -> str:
        return "recursive"

    # ==========================================================
    # Document
    # ==========================================================

    def split(
        self,
        document: Document,
    ) -> List[Chunk]:

        texts = self.split_text(document.content)

        chunks = []

        for index, text in enumerate(texts):

            chunks.append(
                self.create_chunk(
                    document=document,
                    content=text,
                    index=index,
                )
            )

        return chunks

    # ==========================================================
    # Text
    # ==========================================================

    def split_text(
        self,
        text: str,
    ) -> List[str]:

        if not text:
            return []

        return self._recursive_split(
            text=text,
            separators=self.separators,
        )

    # ==========================================================
    # Recursive
    # ==========================================================

    def _recursive_split(
        self,
        text: str,
        separators: List[str],
    ) -> List[str]:

        if len(text) <= self.chunk_size:
            return [text.strip()]

        if not separators:
            return self._fallback.split_text(text)

        separator = separators[0]

        parts = self._split_by_separator(
            text,
            separator,
        )

        if len(parts) <= 1:
            return self._recursive_split(
                text,
                separators[1:],
            )

        chunks = []
        current = ""

        for part in parts:

            if not part:
                continue

            candidate = current + part

            if len(candidate) <= self.chunk_size:

                current = candidate

            else:

                if current.strip():
                    chunks.extend(
                        self._recursive_split(
                            current.strip(),
                            separators[1:],
                        )
                    )

                current = part

        if current.strip():
            chunks.extend(
                self._recursive_split(
                    current.strip(),
                    separators[1:],
                )
            )

        return chunks

    # ==========================================================
    # Helper
    # ==========================================================

    def _split_by_separator(
        self,
        text: str,
        separator: str,
    ) -> List[str]:

        if separator in ("\n", "\n\n", " "):
            return text.split(separator)

        return re.split(separator, text)