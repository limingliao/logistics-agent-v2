"""
ResponseFormatter V3

职责：
- 读取 context.execution_results
- 合并工具结果
- LLM润色输出
- 写入 context.response
"""

from app.agent.context import AgentContext
from app.llm.model import llm
from app.core.logger import logger
from app.agent.prompts import SYSTEM_PROMPT


class ResponseFormatter:

    def format(self, context: AgentContext) -> AgentContext:
        """
        输出最终回复
        """

        logger.info("[Formatter] Start")

        results = context.execution_results

        # =========================
        # fallback
        # =========================
        if not results:

            context.response = self._llm_fallback(context.message)
            return context

        # =========================
        # only llm fallback
        # =========================
        if len(results) == 1 and results[0].tool == "llm":

            context.response = self._llm_fallback(context.message)
            return context

        # =========================
        # merge tool results
        # =========================
        tool_text = self._merge(results)

        # =========================
        # polish with LLM
        # =========================
        context.response = self._polish(context.message, tool_text)

        return context

    # -------------------------------------------------

    def _merge(self, results):
        return "\n".join(
            f"{r.tool}: {r.output}"
            for r in results
            if r.output is not None
        )

    # -------------------------------------------------

    def _polish(self, message, tool_text):

        prompt = f"""
用户问题：
{message}

工具结果：
{tool_text}

请用自然语言回答用户：
1. 不要编造信息
2. 中文输出
3. 不要输出JSON
"""

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]

        return llm.chat_with_messages(messages)

    # -------------------------------------------------

    def _llm_fallback(self, message):

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ]

        return llm.chat_with_messages(messages)