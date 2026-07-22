from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Iterator

from app.llm.llm_result import LLMResult



class BaseLLM(ABC):
    """
    LLM基础抽象类


    所有大模型实现必须继承：

        DeepSeekChat

        OpenAIChat

        OllamaChat

        GeminiChat


    统一接口：

        generate()

        chat()

        stream()

        health_check()

    """



    # =====================================================
    # Properties
    # =====================================================

    @property
    @abstractmethod
    def llm_name(self) -> str:
        """
        模型名称
        """

        pass



    # =====================================================
    # Generate
    # =====================================================

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,

    ) -> LLMResult:
        """
        单次文本生成


        Example:

            result = llm.generate(
                "解释物流赔偿"
            )

        """

        pass



    # =====================================================
    # Chat
    # =====================================================

    @abstractmethod
    def chat(
        self,
        messages: List[Dict[str, str]],

    ) -> LLMResult:
        """
        多轮对话


        messages:

        [
            {
              "role":"user",
              "content":"你好"
            }
        ]

        """

        pass



    # =====================================================
    # Stream
    # =====================================================

    def stream(
        self,
        prompt: str,
    ) -> Iterator[str]:
        """
        流式输出


        默认不实现。

        支持：

        WebSocket
        SSE
        实时客服


        """

        raise NotImplementedError(
            "This LLM does not support streaming."
        )



    # =====================================================
    # Token
    # =====================================================

    def count_tokens(
        self,
        text: str,
    ) -> int:
        """
        Token计算

        默认实现。

        后续可以接入：

        tiktoken

        """

        return len(
            text.split()
        )



    # =====================================================
    # Health
    # =====================================================

    @abstractmethod
    def health_check(
        self,
    ) -> dict:
        """
        服务健康检查
        """

        pass



    # =====================================================
    # Magic
    # =====================================================

    def __repr__(self):

        return (
            f"{self.__class__.__name__}"
            f"(name={self.llm_name})"
        )