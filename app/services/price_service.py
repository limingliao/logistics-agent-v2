"""
运费业务 Service
"""

from app.core.logger import logger
from app.core.exceptions import ValidationException


class PriceService:

    @staticmethod
    def calculate(
        origin: str,
        destination: str,
        weight: float
    ):
        """
        运费计算
        """

        if not origin or not destination:
            raise ValidationException("origin/destination不能为空")

        if weight <= 0:
            raise ValidationException("weight必须大于0")

        logger.info(
            f"[PriceService] 运费计算: "
            f"{origin}->{destination}, weight={weight}"
        )

        # 临时示例算法
        base_price = 10
        unit_price = 2

        total = base_price + weight * unit_price

        return {
            "origin": origin,
            "destination": destination,
            "weight": weight,
            "price": round(total, 2)
        }