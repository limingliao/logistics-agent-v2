"""
Executor

职责：
    1. 执行 Planner 生成的执行计划
    2. 调用 ToolDispatcher
    3. 聚合执行结果
    4. 提供统一执行入口
"""

from typing import Dict, Any, List

from app.core.logger import logger
from app.dispatcher.tool_dispatcher import ToolDispatcher


class Executor:
    """
    企业级 Executor
    """

    def __init__(self):
        self.tool_dispatcher = ToolDispatcher()

    # =====================================================
    # 主入口
    # =====================================================

    def execute(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行 Planner 生成的 Plan

        Args:
            plan: {
                "steps": [...]
            }

        Returns:
            execution result
        """

        logger.info("[Executor] Start Execution")

        steps = plan.get("steps", [])

        results: List[Dict[str, Any]] = []

        for index, step in enumerate(steps):

            tool_name = step.get("tool")
            args = step.get("args", {})

            logger.info(
                f"[Executor] Step {index + 1}: tool={tool_name}, args={args}"
            )

            try:

                # =========================
                # 1. LLM fallback step
                # =========================
                if tool_name is None:
                    logger.info("[Executor] LLM fallback step")

                    results.append({
                        "tool": "llm",
                        "output": "fallback_to_llm"
                    })

                    continue

                # =========================
                # 2. Tool execution
                # =========================
                output = self.tool_dispatcher.dispatch(
                    tool_name,
                    **args
                )

                results.append({
                    "tool": tool_name,
                    "input": args,
                    "output": output
                })

            except Exception as e:

                logger.exception(f"[Executor] Step failed: {tool_name}")

                results.append({
                    "tool": tool_name,
                    "input": args,
                    "error": str(e)
                })

        final_result = {
            "steps": steps,
            "results": results
        }

        logger.info("[Executor] Execution Finished")

        return final_result