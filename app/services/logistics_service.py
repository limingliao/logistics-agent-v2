"""
物流业务
"""

from app.agent.tools import query_track


class LogisticsService:

    @staticmethod
    def get_tracks(order_no: str):

        return query_track(order_no)