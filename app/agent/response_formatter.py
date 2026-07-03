"""
Response Formatter

负责：

1. Tool Result Normalize
2. Tool Result Merge
3. LLM Polish
4. Final Response
"""

from typing import Any, Dict, List

from app.agent.prompts import SYSTEM_PROMPT
from app.core.logger import logger
from app.llm.model import llm


class ResponseFormatter:

    def format(
        self,
        context: Dict[str, Any],
        execution_result: Dict[str, Any]
    ) -> str:
        """
        对外统一入口
        """

        logger.info("[ResponseFormatter] Start")

        results = execution_result.get("results", [])

        # 没有任何结果
        if not results:
            return self._fallback(context)

        # 只有LLM
        if (
            len(results) == 1
            and results[0].get("tool") == "llm"
        ):
            return self._fallback(context)

        # Tool结果整理
        merged_result = self._merge_results(results)

        # LLM润色
        return self._polish(
            context=context,
            tool_result=merged_result
        )

    # ===================================================

    def _merge_results(
        self,
        results: List[Dict[str, Any]]
    ) -> str:
        """
        多Tool结果统一整理
        """

        logger.info("[Formatter] Merge Tool Results")

        contents = []

        for item in results:

            if "output" in item:

                contents.append(
                    f"{item['tool']}：{item['output']}"
                )

        return "\n".join(contents)

    # ===================================================

    def _polish(
        self,
        context: Dict[str, Any],
        tool_result: str
    ) -> str:
        """
        LLM整理Tool输出
        """

        logger.info("[Formatter] Polish")

        prompt = f"""
用户问题：

{context["message"]}

下面是工具返回结果：

{tool_result}

请根据工具返回结果回答用户。

要求：

1. 不要编造信息
2. 语言自然
3. 中文回答
4. 不暴露JSON
"""

        messages = [

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": prompt
            }

        ]

        return llm.chat_with_messages(messages)

    # ===================================================

    def _fallback(
        self,
        context: Dict[str, Any]
    ) -> str:
        """
        Tool未命中
        """

        logger.info("[Formatter] Fallback")

        messages = [

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": context["message"]
            }

        ]

        return llm.chat_with_messages(messages)