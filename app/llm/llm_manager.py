from __future__ import annotations

from typing import Dict, Optional

from llm.base_llm import BaseLLM


class LLMManager:
    """
    LLM 管理器

    负责：

    1. 注册模型
    2. 获取模型
    3. 管理默认模型
    4. 统一调用入口


    Example:

        llm_manager.register(
            "deepseek",
            DeepSeekChat(...)
        )


        llm = llm_manager.get(
            "deepseek"
        )

    """

    def __init__(self):

        # 存储所有LLM实例
        self._llms: Dict[str, BaseLLM] = {}

        # 默认LLM
        self._default_llm: Optional[str] = None



    # =====================================================
    # Register
    # =====================================================

    def register(
        self,
        name: str,
        llm: BaseLLM,
        default: bool = False,
    ) -> BaseLLM:
        """
        注册LLM

        """

        if not isinstance(
            llm,
            BaseLLM
        ):
            raise TypeError(
                "llm must inherit BaseLLM"
            )


        self._llms[name] = llm


        # 第一个自动成为默认
        if (
            default
            or
            self._default_llm is None
        ):
            self._default_llm = name


        return llm



    # =====================================================
    # Get
    # =====================================================

    def get(
        self,
        name: Optional[str] = None,
    ) -> BaseLLM:
        """
        获取LLM实例

        """

        name = (
            name
            or
            self._default_llm
        )


        if name is None:

            raise RuntimeError(
                "No LLM registered."
            )


        llm = self._llms.get(
            name
        )


        if llm is None:

            raise KeyError(
                f"LLM '{name}' not found."
            )


        return llm



    # =====================================================
    # Remove
    # =====================================================

    def remove(
        self,
        name: str,
    ):

        if name in self._llms:

            del self._llms[name]


        if self._default_llm == name:

            self._default_llm = None



    # =====================================================
    # Generate
    # =====================================================

    def generate(
        self,
        prompt: str,
        llm_name: Optional[str] = None,
        system_prompt: Optional[str] = None,
    ):
        """
        统一生成入口


        Agent 不需要知道具体模型。

        """

        llm = self.get(
            llm_name
        )


        return llm.generate(
            prompt=prompt,
            system_prompt=system_prompt,
        )



    # =====================================================
    # Chat
    # =====================================================

    def chat(
        self,
        messages,
        llm_name: Optional[str] = None,
    ):

        llm = self.get(
            llm_name
        )


        return llm.chat(
            messages
        )



    # =====================================================
    # Stream
    # =====================================================

    def stream(
        self,
        prompt: str,
        llm_name: Optional[str] = None,
    ):

        llm = self.get(
            llm_name
        )


        return llm.stream(
            prompt
        )



    # =====================================================
    # Health Check
    # =====================================================

    def health_check(self):

        result = {}


        for name, llm in self._llms.items():

            result[name] = (
                llm.health_check()
            )


        return result



    # =====================================================
    # Info
    # =====================================================

    def list_models(self):

        return list(
            self._llms.keys()
        )


    def statistics(self):

        return {

            "count":
                len(self._llms),

            "default":
                self._default_llm,

            "models":
                self.list_models()

        }



    # =====================================================
    # Magic
    # =====================================================

    def __len__(self):

        return len(
            self._llms
        )


    def __repr__(self):

        return (
            f"LLMManager("
            f"models={list(self._llms.keys())}"
            f")"
        )