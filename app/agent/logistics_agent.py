from __future__ import annotations

from typing import Any, Dict, Optional

from app.agent.base_agent import BaseAgent



class LogisticsAgent(BaseAgent):
    """
    物流智能客服Agent


    能力：

    - 订单查询
    - 物流查询
    - 知识库问答
    - 智能回复


    """

    def __init__(
        self,
        **kwargs
    ):

        super().__init__(
            name="logistics_agent",
            **kwargs
        )



    # =====================================================
    # Main Entry
    # =====================================================

    def run(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None,
    ):

        context = context or {}


        # --------------------------------
        # 1. 获取历史记忆
        # --------------------------------

        history = self._get_history(
            context
        )


        # --------------------------------
        # 2. 意图识别
        # --------------------------------

        intent = self._detect_intent(
            message
        )


        # --------------------------------
        # 3. 执行业务
        # --------------------------------

        tool_result = None

        rag_result = None



        if intent == "order_query":

            tool_result = (
                self._query_order(
                    message
                )
            )


        elif intent == "knowledge":

            rag_result = (
                self.retrieve(
                    message
                )
            )


        elif intent == "complex":

            tool_result = (
                self._query_order(
                    message
                )
            )

            rag_result = (
                self.retrieve(
                    message
                )
            )


        # --------------------------------
        # 4. 构建Prompt
        # --------------------------------

        prompt = self._build_prompt(

            message=message,

            history=history,

            tool_result=tool_result,

            rag_result=rag_result,

        )


        # --------------------------------
        # 5. LLM生成
        # --------------------------------

        result = self.generate(
            prompt,
            system_prompt=self.system_prompt()
        )


        # --------------------------------
        # 6. 保存记忆
        # --------------------------------

        self.remember(

            key="last_message",

            value={
                "user":message,
                "assistant":result.text
            }

        )


        return result



    # =====================================================
    # Intent
    # =====================================================

    def _detect_intent(
        self,
        message:str
    ):

        keywords = {


            "order_query":[
                "订单",
                "物流",
                "在哪里",
                "到哪",
                "什么时候到",
                "运输"
            ],


            "knowledge":[

                "赔偿",
                "规则",
                "多少钱",
                "怎么办",
                "政策"

            ]

        }



        for intent, words in keywords.items():

            for word in words:

                if word in message:

                    return intent



        return "complex"



    # =====================================================
    # Tool Query
    # =====================================================

    def _query_order(
        self,
        message:str
    ):

        """
        调用订单查询Tool


        """

        if not self.tool_manager:

            return None


        try:

            return self.execute_tool(

                "query_order",

                message=message

            )


        except Exception as e:

            return {

                "error":str(e)

            }



    # =====================================================
    # Prompt
    # =====================================================

    def _build_prompt(
        self,
        message,
        history=None,
        tool_result=None,
        rag_result=None,
    ):


        prompt = f"""

你是一名专业物流客服。

请根据以下信息回答用户。


用户问题：

{message}


"""


        if history:

            prompt += f"""

历史对话：

{history}

"""


        if tool_result:

            prompt += f"""

订单查询结果：

{tool_result}

"""


        if rag_result:

            prompt += f"""

知识库资料：

{rag_result}

"""


        prompt += """

要求：

1. 回复准确
2. 不确定的信息不要编造
3. 使用客服语气
4. 简洁清晰


"""


        return prompt



    # =====================================================
    # Memory
    # =====================================================

    def _get_history(
        self,
        context
    ):

        if not self.memory_manager:

            return None


        return self.recall(
            "last_message"
        )



    # =====================================================
    # System Prompt
    # =====================================================

    def system_prompt(self):

        return """

你是物流行业智能客服助手。

你的职责：

- 查询订单
- 查询物流状态
- 解答物流政策
- 帮助用户解决配送问题


"""



    # =====================================================
    # Health
    # =====================================================

    def health_check(self):

        return {

            "agent":
                self.name,

            "status":
                "running"

        }