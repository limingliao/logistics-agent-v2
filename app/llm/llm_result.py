from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class LLMResult:
    """
    LLM生成结果


    Flow:

        Prompt

          ↓

        LLM

          ↓

        LLMResult


    """

    # =====================================================
    # Response Text
    # =====================================================

    text: str


    # =====================================================
    # Model Info
    # =====================================================

    model: str = ""


    # =====================================================
    # Statistics
    # =====================================================

    elapsed: float = 0.0


    # =====================================================
    # Metadata
    # =====================================================

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


    # =====================================================
    # Error
    # =====================================================

    error: Optional[str] = None



    # =====================================================
    # Properties
    # =====================================================

    @property
    def success(self) -> bool:
        """
        是否生成成功
        """

        return (
            self.error is None
            and
            bool(self.text)
        )


    @property
    def failed(self) -> bool:

        return not self.success



    @property
    def token_usage(self):
        """
        Token消耗

        DeepSeek/OpenAI:

        {
            prompt_tokens,
            completion_tokens,
            total_tokens
        }

        """

        usage = self.metadata.get(
            "usage"
        )

        return usage



    # =====================================================
    # Metadata
    # =====================================================

    def set_metadata(
        self,
        key: str,
        value: Any,
    ):

        self.metadata[key] = value



    def get_metadata(
        self,
        key: str,
        default=None,
    ):

        return self.metadata.get(
            key,
            default
        )



    # =====================================================
    # Factory
    # =====================================================

    @classmethod
    def failure(
        cls,
        error: str,
        model: str = "",
    ):
        """
        创建失败结果
        """

        return cls(
            text="",
            model=model,
            error=error,
        )



    # =====================================================
    # Serialization
    # =====================================================

    def to_dict(self):

        return {

            "text": self.text,

            "model": self.model,

            "success": self.success,

            "elapsed": self.elapsed,

            "error": self.error,

            "metadata": self.metadata,

        }



    # =====================================================
    # Magic Methods
    # =====================================================

    def __bool__(self):

        return self.success



    def __len__(self):

        return len(
            self.text
        )



    def __repr__(self):

        return (
            f"LLMResult("
            f"model='{self.model}', "
            f"success={self.success}, "
            f"elapsed={self.elapsed:.4f}s)"
        )