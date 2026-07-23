from __future__ import annotations

from typing import Dict, Optional

from app.agent.base_agent import BaseAgent


class AgentManager:
    """
    Agent管理器

    负责：

    - 注册Agent
    - 获取Agent
    - 管理默认Agent
    - 统一调用入口

    """


    def __init__(self):

        self._agents: Dict[str, BaseAgent] = {}

        self._default_agent: Optional[str] = None



    # =====================================================
    # Register
    # =====================================================

    def register(
        self,
        name: str,
        agent: BaseAgent,
        default: bool = False,
    ):

        if not isinstance(
            agent,
            BaseAgent
        ):
            raise TypeError(
                "agent must inherit BaseAgent"
            )


        self._agents[name] = agent


        if (
            default
            or
            self._default_agent is None
        ):

            self._default_agent = name


        return agent



    # =====================================================
    # Get
    # =====================================================

    def get(
        self,
        name: Optional[str] = None,
    ) -> BaseAgent:


        name = (
            name
            or
            self._default_agent
        )


        if name is None:

            raise RuntimeError(
                "No agent registered"
            )


        agent = self._agents.get(
            name
        )


        if agent is None:

            raise KeyError(
                f"Agent {name} not found"
            )


        return agent



    # =====================================================
    # Run
    # =====================================================

    def run(
        self,
        message: str,
        agent_name: Optional[str] = None,
        context=None,
    ):

        agent = self.get(
            agent_name
        )


        return agent.run(
            message,
            context
        )



    # =====================================================
    # Health
    # =====================================================

    def health_check(self):

        return {

            name:
                agent.health_check()

            for name, agent

            in self._agents.items()

        }



    # =====================================================
    # Info
    # =====================================================

    def list_agents(self):

        return list(
            self._agents.keys()
        )


    def __len__(self):

        return len(
            self._agents
        )


    def __repr__(self):

        return (
            f"AgentManager("
            f"{self.list_agents()}"
            f")"
        )