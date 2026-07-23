from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseAgent(ABC):
    """
    Agent基础抽象类


    所有业务Agent继承：

        LogisticsAgent

        CustomerServiceAgent

        QAAgent


    Agent负责：

        1. 接收用户请求
        2. 调度能力模块
        3. 返回结果


    """

    def __init__(
        self,
        name: str,

        llm_manager=None,

        memory_manager=None,

        workflow_manager=None,

        tool_manager=None,

        rag_manager=None,

    ):

        self.name = name


        # ----------------------------
        # Core Components
        # ----------------------------

        self.llm_manager = (
            llm_manager
        )

        self.memory_manager = (
            memory_manager
        )

        self.workflow_manager = (
            workflow_manager
        )

        self.tool_manager = (
            tool_manager
        )

        self.rag_manager = (
            rag_manager
        )



    # =====================================================
    # Properties
    # =====================================================

    @property
    def agent_name(self):

        return self.name



    # =====================================================
    # Main Entry
    # =====================================================

    @abstractmethod
    def run(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None,
    ):
        """
        Agent执行入口


        Example:

            result = agent.run(
                "我的订单在哪里"
            )

        """

        pass



    # =====================================================
    # LLM
    # =====================================================

    def generate(
        self,
        prompt: str,
        system_prompt: str = None,
    ):

        if not self.llm_manager:

            raise RuntimeError(
                "LLMManager not initialized"
            )


        return self.llm_manager.generate(
            prompt=prompt,
            system_prompt=system_prompt,
        )



    # =====================================================
    # Memory
    # =====================================================

    def remember(
        self,
        key: str,
        value: Any,
    ):

        if not self.memory_manager:

            return


        return self.memory_manager.save(
            key,
            value
        )



    def recall(
        self,
        key: str,
    ):

        if not self.memory_manager:

            return None


        return self.memory_manager.get(
            key
        )



    # =====================================================
    # Tool
    # =====================================================

    def execute_tool(
        self,
        tool_name: str,
        **kwargs
    ):

        if not self.tool_manager:

            raise RuntimeError(
                "ToolManager not initialized"
            )


        return self.tool_manager.execute(
            tool_name,
            **kwargs
        )



    # =====================================================
    # RAG
    # =====================================================

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ):

        if not self.rag_manager:

            return None


        return self.rag_manager.query(
            query=query,
            top_k=top_k,
        )



    # =====================================================
    # Workflow
    # =====================================================

    def execute_workflow(
        self,
        workflow_name: str,
        context: dict,
    ):

        if not self.workflow_manager:

            raise RuntimeError(
                "WorkflowManager not initialized"
            )


        return self.workflow_manager.execute(
            workflow_name,
            context
        )



    # =====================================================
    # Lifecycle
    # =====================================================

    def health_check(self):

        return {

            "agent":
                self.name,

            "status":
                "ok"

        }



    # =====================================================
    # Magic
    # =====================================================

    def __repr__(self):

        return (
            f"{self.__class__.__name__}"
            f"(name={self.name})"
        )