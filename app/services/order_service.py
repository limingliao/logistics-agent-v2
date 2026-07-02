"""
订单业务 Service（企业级）
"""

from sqlalchemy.orm import Session

from app.core.logger import logger
from app.core.exceptions import OrderNotFoundException
from app.database.repository import LogisticsRepository


class OrderService:

    @staticmethod
    def get_order_detail(db: Session, order_no: str):

        if not order_no:
            raise OrderNotFoundException("订单号不能为空")

        logger.info(f"[OrderService] get order: {order_no}")

        order = LogisticsRepository.get_order_detail(
            db=db,
            order_no=order_no
        )

        if not order:
            logger.warning(f"[OrderService] order not found: {order_no}")
            raise OrderNotFoundException()

        logger.info(f"[OrderService] success: {order_no}")

        return order