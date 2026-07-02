"""
物流业务 Service
"""

from app.core.logger import logger
from app.core.exceptions import ValidationException
# from app.agent.tools import query_track


class LogisticsService:

    @staticmethod
    def get_tracks(order_no: str):

        if not order_no:
            raise ValidationException("order_no不能为空")

        logger.info(f"[LogisticsService] query track: {order_no}")

        try:
            # result = query_track(order_no)

            logger.info(f"[LogisticsService] success: {order_no}")

            # return result

        except Exception as e:
            logger.exception(f"[LogisticsService] failed: {order_no}")
            raise