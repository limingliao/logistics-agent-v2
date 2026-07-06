from __future__ import annotations

from typing import List

from rag.chunk import Chunk
from rag.document import Document
from rag.splitters.base_splitter import BaseSplitter


class TextSplitter(BaseSplitter):
    """
    基础文本切分器

    使用固定长度 + overlap 的方式进行切分。

    示例：

        chunk_size = 500
        overlap = 50

        ------------------------
        | 0 ~ 500             |
               ------------------------
               |450 ~ 950            |
                      ------------------------
                      |900 ~ 1400          |
    """

    @property
    def splitter_name(self) -> str:
        return "text"

    # ==========================================================
    # Split Document
    # ==========================================================

    def split(
        self,
        document: Document,
    ) -> List[Chunk]:
        """
        Document -> Chunk
        """

        texts = self.split_text(document.content)

        chunks: List[Chunk] = []

        for index, text in enumerate(texts):
            chunk = self.create_chunk(
                document=document,
                content=text,
                index=index,
            )
            chunks.append(chunk)

        return chunks

    # ==========================================================
    # Split Text
    # ==========================================================

    def split_text(
        self,
        text: str,
    ) -> List[str]:
        """
        固定长度切分文本
        """

        if not text:
            return []

        if len(text) <= self.chunk_size:
            return [text]

        chunks: List[str] = []

        step = self.chunk_size - self.chunk_overlap

        start = 0

        while start < len(text):

            end = min(
                start + self.chunk_size,
                len(text),
            )

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            if end >= len(text):
                break

            start += step

        return chunks

    # ==========================================================
    # Statistics
    # ==========================================================

    def estimate_chunk_count(
        self,
        text: str,
    ) -> int:
        """
        预估Chunk数量
        """

        if not text:
            return 0

        if len(text) <= self.chunk_size:
            return 1

        step = self.chunk_size - self.chunk_overlap

        count = (
            len(text) - self.chunk_overlap + step - 1
        ) // step

        return max(count, 1)