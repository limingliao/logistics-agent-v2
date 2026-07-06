"""
物流业务 Service
"""

from app.core.logger import logger
from app.core.exceptions import ValidationException
# from app.agent.tools import query_track
from sqlalchemy.orm import Session



class LogisticsService:
    @staticmethod
    def get_order_detail(
            db: Session,
            order_no: str
    ):
        """
        查询订单及物流轨迹
        """

        if not order_no:
            raise ValidationException("order_no不能为空")

        logger.info(f"[LogisticsService] 查询物流: {order_no}")

        result = LogisticsRepository.get_order_detail(
            db=db,
            order_no=order_no
        )

        if result is None:
            raise ValidationException("订单不存在")

        logger.info(f"[LogisticsService] 查询成功: {order_no}")

        return result

    @staticmethod
    def get_tracks(order_no: str):
        """
        查询物流轨迹
        """
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