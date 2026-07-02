"""
运费 Tool
"""

from app.services.price_service import PriceService


def calculate_price_tool(
    origin,
    destination,
    weight
):
    """
    运费计算
    """

    return PriceService.calculate(
        origin=origin,
        destination=destination,
        weight=weight
    )