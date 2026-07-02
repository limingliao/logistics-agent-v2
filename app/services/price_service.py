"""
运费业务
"""

from app.agent.tools import query_price


class PriceService:

    @staticmethod
    def calculate(
        origin,
        destination,
        weight
    ):

        return query_price(
            origin,
            destination,
            weight
        )