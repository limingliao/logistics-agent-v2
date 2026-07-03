"""
Tool Registry

自动注册所有 Tool。
"""

from typing import Callable


class ToolRegistry:
    """
    Tool 注册中心
    """

    _tools: dict[str, Callable] = {}

    @classmethod
    def register(cls, name: str):
        """
        Tool 注册装饰器
        """

        def decorator(func: Callable):

            if name in cls._tools:
                raise ValueError(
                    f"Tool '{name}' 已存在"
                )

            cls._tools[name] = func

            return func

        return decorator

    @classmethod
    def get(cls, name: str):

        return cls._tools.get(name)

    @classmethod
    def has(cls, name: str):

        return name in cls._tools

    @classmethod
    def list_tools(cls):

        return list(cls._tools.keys())

    @classmethod
    def get_all(cls):

        return cls._tools