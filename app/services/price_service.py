"""
运费业务 Service
"""

from app.core.logger import logger
from app.core.exceptions import ValidationException
from app.agent.tools import query_price


class PriceService:

    @staticmethod
    def calculate(origin, destination, weight):

        if not origin or not destination:
            raise ValidationException("origin/destination不能为空")

        if weight <= 0:
            raise ValidationException("weight必须大于0")

        logger.info(
            f"[PriceService] calc price: {origin} -> {destination}, weight={weight}"
        )

        try:
            result = query_price(origin, destination, weight)

            logger.info("[PriceService] success")

            return result

        except Exception as e:
            logger.exception("[PriceService] failed")
            raise