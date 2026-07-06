"""
Tool Dispatcher

统一负责 Tool 分发，不关心 Tool 的具体实现。
"""

from typing import Any

from app.agent.tools.registry import ToolRegistry


class ToolDispatcher:
    """
    Tool 调度器
    """

    @staticmethod
    def dispatch(
        tool_name: str,
        **kwargs: Any
    ):
        """
        根据 Tool 名称调用对应 Tool。

        Args:
            tool_name: Tool 名称
            **kwargs: Tool 参数

        Returns:
            Tool 执行结果
        """

        tool = ToolRegistry.get(tool_name)

        if tool is None:
            raise ValueError(
                f"Unknown tool: {tool_name}"
            )

        return tool(**kwargs)

    @staticmethod
    def has_tool(
        tool_name: str
    ) -> bool:
        """
        判断 Tool 是否存在
        """

        return tool_name in ToolRegistry

    @staticmethod
    def list_tools():
        """
        返回所有 Tool 名称
        """

        return list(ToolRegistry.keys())