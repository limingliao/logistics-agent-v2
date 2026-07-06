"""
订单业务 Service
"""

from sqlalchemy.orm import Session

from app.core.logger import logger
from app.core.exceptions import OrderNotFoundException
from app.database.repository import OrderRepository


class OrderService:

    @staticmethod
    def get_order(
        db: Session,
        order_no: str
    ):
        """
        查询订单
        """

        if not order_no:
            raise OrderNotFoundException("订单号不能为空")

        logger.info(f"[OrderService] 查询订单: {order_no}")

        order = OrderRepository.get_order(
            db=db,
            order_no=order_no
        )

        if order is None:
            logger.warning(f"[OrderService] 订单不存在: {order_no}")
            raise OrderNotFoundException()

        logger.info(f"[OrderService] 查询成功: {order_no}")

        return order