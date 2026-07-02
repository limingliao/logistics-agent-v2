"""
物流 Tool
"""

from sqlalchemy.orm import Session

from app.services.logistics_service import LogisticsService


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