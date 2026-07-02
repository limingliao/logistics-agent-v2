"""
订单业务
"""

from app.agent.tools import query_order


class OrderService:

    @staticmethod
    def get_order(order_no: str):

        return query_order(order_no)