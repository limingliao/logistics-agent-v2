"""
运费 Tool
"""
from app.agent.tools.registry import ToolRegistry
from app.services.price_service import PriceService

@ToolRegistry.register("calculate_price")
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