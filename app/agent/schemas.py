"""
schemas.py

定义所有 LLM Tool Schema

作用：
    告诉大模型有哪些工具可以调用
"""

# ============================================================
# 查询订单
# ============================================================

QUERY_ORDER_TOOL = {
    "type": "function",
    "function": {
        "name": "query_order",
        "description": "根据订单号查询物流订单详情",
        "parameters": {
            "type": "object",
            "properties": {
                "order_no": {
                    "type": "string",
                    "description": "物流订单号，例如：SF10001"
                }
            },
            "required": [
                "order_no"
            ]
        }
    }
}


# ============================================================
# 查询物流轨迹（V2.3）
# ============================================================

QUERY_TRACK_TOOL = {
    "type": "function",
    "function": {
        "name": "query_track",
        "description": "根据订单号查询物流轨迹",
        "parameters": {
            "type": "object",
            "properties": {
                "order_no": {
                    "type": "string",
                    "description": "物流订单号"
                }
            },
            "required": [
                "order_no"
            ]
        }
    }
}


# ============================================================
# 查询运费（V2.3）
# ============================================================

QUERY_PRICE_TOOL = {
    "type": "function",
    "function": {
        "name": "query_price",
        "description": "根据起点、终点、重量查询物流运费",
        "parameters": {
            "type": "object",
            "properties": {
                "sender_city": {
                    "type": "string",
                    "description": "寄件城市"
                },
                "receiver_city": {
                    "type": "string",
                    "description": "收件城市"
                },
                "weight": {
                    "type": "number",
                    "description": "重量（kg）"
                }
            },
            "required": [
                "sender_city",
                "receiver_city",
                "weight"
            ]
        }
    }
}


# ============================================================
# 转人工客服（预留）
# ============================================================

TRANSFER_TO_HUMAN_TOOL = {
    "type": "function",
    "function": {
        "name": "transfer_to_human",
        "description": "当用户要求人工客服或模型无法解决问题时调用",
        "parameters": {
            "type": "object",
            "properties": {
                "reason": {
                    "type": "string",
                    "description": "转人工原因"
                }
            },
            "required": [
                "reason"
            ]
        }
    }
}


# ============================================================
# Tool 列表
# ============================================================

TOOLS = [
    QUERY_ORDER_TOOL,
    QUERY_TRACK_TOOL,
    QUERY_PRICE_TOOL,
    TRANSFER_TO_HUMAN_TOOL,
]