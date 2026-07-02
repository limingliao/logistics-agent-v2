"""
registry.py

Tool Registry
负责根据 LLM 返回的 Tool 名称执行对应 Python 函数
"""

import json
from typing import Any, Callable

from sqlalchemy.orm import Session

from app.agent.tools import LogisticsTools


class ToolRegistry:
    """
    Tool 注册中心
    """

    # =====================================================
    # Tool 映射
    # =====================================================

    TOOL_MAPPING: dict[str, Callable[..., Any]] = {
        "query_order": LogisticsTools.query_order,
    }

    # =====================================================
    # 执行 Tool
    # =====================================================

    @classmethod
    def execute(
        cls,
        db: Session,
        function_name: str,
        arguments,
    ) -> dict:
        """
        执行 Tool

        Args:
            db: 数据库 Session
            function_name: Tool 名称
            arguments: Tool 参数（dict 或 JSON 字符串）

        Returns:
            dict
        """

        # ---------- 参数解析 ----------
        if isinstance(arguments, str):
            try:
                arguments = json.loads(arguments)
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "message": "Tool 参数解析失败"
                }

        # ---------- 查找 Tool ----------
        tool = cls.TOOL_MAPPING.get(function_name)

        if tool is None:
            return {
                "success": False,
                "message": f"未知工具：{function_name}"
            }

        # ---------- 执行 Tool ----------
        try:
            return tool(
                db=db,
                **arguments
            )

        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }

    # =====================================================
    # 注册 Tool（后续动态扩展）
    # =====================================================

    @classmethod
    def register(
        cls,
        name: str,
        func: Callable[..., Any],
    ):
        """
        注册 Tool
        """

        cls.TOOL_MAPPING[name] = func

    # =====================================================
    # 获取所有 Tool
    # =====================================================

    @classmethod
    def list_tools(cls):

        return list(cls.TOOL_MAPPING.keys())