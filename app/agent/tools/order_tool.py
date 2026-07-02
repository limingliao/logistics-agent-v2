"""
订单 Tool
"""

from sqlalchemy.orm import Session

from app.services.order_service import OrderService


def get_order_tool(
    db: Session,
    order_no: str
):
    """
    Agent 调用：
    查询订单
    """

    return OrderService.get_order(
        db=db,
        order_no=order_no
    )