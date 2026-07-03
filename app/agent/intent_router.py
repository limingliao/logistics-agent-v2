"""
Intent Router

负责识别用户意图，不负责业务执行。

职责：
    1. Intent Classification
    2. Entity Extraction（后续）
    3. Confidence（后续）
"""

from dataclasses import dataclass
from typing import Dict

from app.core.logger import logger


# ===========================
# Intent 常量
# ===========================

ORDER_QUERY = "ORDER_QUERY"
TRACK_QUERY = "TRACK_QUERY"
PRICE_QUERY = "PRICE_QUERY"
GENERAL_CHAT = "GENERAL_CHAT"


# ===========================
# Router Result
# ===========================

@dataclass
class IntentResult:
    """
    Router 返回结果
    """

    intent: str
    confidence: float
    entities: Dict


# ===========================
# Intent Router
# ===========================

class IntentRouter:
    """
    企业级 Intent Router

    当前：
        Keyword Rule

    后续：
        DeepSeek
        GPT
        Qwen
        Intent Classifier
    """

    def route(self, message: str) -> IntentResult:
        """
        Intent Routing

        Args:
            message: 用户输入

        Returns:
            IntentResult
        """

        logger.info("[Router] Start Routing")

        message = message.strip()

        # -------------------------------
        # Order
        # -------------------------------
        if any(keyword in message for keyword in [
            "订单",
            "下单",
            "订单号"
        ]):

            result = IntentResult(
                intent=ORDER_QUERY,
                confidence=0.95,
                entities={}
            )

        # -------------------------------
        # Track
        # -------------------------------
        elif any(keyword in message for keyword in [
            "物流",
            "快递",
            "运输",
            "配送",
            "到哪",
            "到哪里",
            "签收"
        ]):

            result = IntentResult(
                intent=TRACK_QUERY,
                confidence=0.95,
                entities={}
            )

        # -------------------------------
        # Price
        # -------------------------------
        elif any(keyword in message for keyword in [
            "价格",
            "报价",
            "费用",
            "多少钱",
            "运费"
        ]):

            result = IntentResult(
                intent=PRICE_QUERY,
                confidence=0.95,
                entities={}
            )

        # -------------------------------
        # General Chat
        # -------------------------------
        else:

            result = IntentResult(
                intent=GENERAL_CHAT,
                confidence=0.60,
                entities={}
            )

        logger.info(
            f"[Router] Intent={result.intent}, Confidence={result.confidence}"
        )

        return result