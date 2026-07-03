"""
订单 Tool
"""

from sqlalchemy.orm import Session

from app.agent.tools.registry import ToolRegistry
from app.services.order_service import OrderService



@ToolRegistry.register("get_order")
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