from __future__ import annotations

import time
from typing import List, Dict, Optional

from openai import OpenAI

from app.llm.base_llm import BaseLLM
from app.llm.llm_result import LLMResult



class DeepSeekChat(BaseLLM):
    """
    DeepSeek Chat 模型实现


    调用流程：

        Prompt

          ↓

        DeepSeek API

          ↓

        LLMResult

    """


    def __init__(
        self,
        api_key: str,
        model: str = "deepseek-chat",
        base_url: str = "https://api.deepseek.com",

        temperature: float = 0.7,

        max_tokens: int = 2048,

    ):

        self.api_key = api_key

        self.model = model

        self.temperature = temperature

        self.max_tokens = max_tokens


        self.client = OpenAI(

            api_key=api_key,

            base_url=base_url

        )



    # ======================================================
    # Properties
    # ======================================================

    @property
    def llm_name(self):

        return "deepseek"



    # ======================================================
    # Generate
    # ======================================================

    def generate(
        self,
        prompt: str,

        system_prompt: Optional[str] = None,

    ) -> LLMResult:
        """
        单轮生成
        """

        start = time.perf_counter()


        messages = []


        if system_prompt:

            messages.append(
                {
                    "role":"system",
                    "content":system_prompt
                }
            )


        messages.append(
            {
                "role":"user",
                "content":prompt
            }
        )



        response = self.client.chat.completions.create(

            model=self.model,

            messages=messages,

            temperature=self.temperature,

            max_tokens=self.max_tokens,

        )



        content = (
            response
            .choices[0]
            .message
            .content
        )



        elapsed = (
            time.perf_counter()
            -
            start
        )



        return LLMResult(

            text=content,

            model=self.model,

            elapsed=elapsed,

            metadata={

                "provider":"deepseek",

                "usage":
                    response.usage.model_dump()
                    if response.usage
                    else None

            }

        )



    # ======================================================
    # Chat
    # ======================================================

    def chat(
        self,

        messages: List[Dict[str,str]]

    ) -> LLMResult:
        """
        多轮聊天
        """


        start = time.perf_counter()



        response = self.client.chat.completions.create(

            model=self.model,

            messages=messages,

            temperature=self.temperature,

            max_tokens=self.max_tokens,

        )



        content = (
            response
            .choices[0]
            .message
            .content
        )



        return LLMResult(

            text=content,

            model=self.model,

            elapsed=
                time.perf_counter()
                -
                start,

            metadata={

                "provider":"deepseek",

                "mode":"chat"

            }

        )



    # ======================================================
    # Streaming
    # ======================================================

    def stream(
        self,

        prompt:str,

    ):

        """
        流式输出

        给 WebSocket 使用
        """

        response = self.client.chat.completions.create(

            model=self.model,

            messages=[

                {
                    "role":"user",
                    "content":prompt
                }

            ],

            stream=True,

            temperature=self.temperature,

        )


        for chunk in response:

            delta = (
                chunk
                .choices[0]
                .delta
                .content
            )


            if delta:

                yield delta



    # ======================================================
    # Health
    # ======================================================

    def health_check(self):

        try:

            result = self.generate(
                "hello"
            )

            return {

                "status":"ok",

                "model":self.model

            }


        except Exception as e:

            return {

                "status":"error",

                "message":str(e)

            }



    # ======================================================
    # Magic
    # ======================================================

    def __repr__(self):

        return (

            f"DeepSeekChat("

            f"model='{self.model}')"

        )