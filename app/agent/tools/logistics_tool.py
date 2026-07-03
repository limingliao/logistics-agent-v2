"""
物流 Tool
"""

from sqlalchemy.orm import Session

from app.agent.tools.registry import ToolRegistry
from app.services.logistics_service import LogisticsService


@ToolRegistry.register("query_track")
def query_track_tool(
    db: Session,
    order_no: str
):
    """
    查询物流
    """

    return LogisticsService.get_order_detail(
        db=db,
        order_no=order_no
    )