"""
Executor V3

职责：
- 执行 context.plan
- 写入 context.execution_results
"""

from app.agent.context import AgentContext, ExecutionItem
from app.dispatcher.tool_dispatcher import ToolDispatcher
from app.core.logger import logger


class Executor:

    def __init__(self):
        self.dispatcher = ToolDispatcher()

    def execute(self, context: AgentContext) -> AgentContext:
        """
        执行计划
        """

        logger.info("[Executor] Start")

        results = []

        for i, step in enumerate(context.plan):

            tool = step.tool
            args = step.args

            logger.info(f"[Executor] Step {i+1} tool={tool}")

            # =========================
            # LLM fallback
            # =========================
            if tool is None:

                results.append(
                    ExecutionItem(
                        tool="llm",
                        input={},
                        output="fallback"
                    )
                )

                continue

            # =========================
            # Tool execution
            # =========================
            try:

                output = self.dispatcher.dispatch(
                    tool,
                    **args
                )

                results.append(
                    ExecutionItem(
                        tool=tool,
                        input=args,
                        output=output
                    )
                )

            except Exception as e:

                logger.exception(f"[Executor] error in {tool}")

                results.append(
                    ExecutionItem(
                        tool=tool,
                        input=args,
                        error=str(e)
                    )
                )

        context.execution_results = results

        logger.info("[Executor] Done")

        return context