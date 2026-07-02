"""
数据仓库层（Repository）

负责组合多个 CRUD，
向 Service 提供完整业务数据。
"""

from sqlalchemy.orm import Session

from app.database.crud import (
    OrderCRUD,
    TrackCRUD,
)


class LogisticsRepository:

    @staticmethod
    def get_order_detail(
        db: Session,
        order_no: str
    ):

        order = OrderCRUD.get_by_order_no(
            db,
            order_no
        )

        if not order:
            return None

        tracks = TrackCRUD.get_tracks(
            db,
            order.id
        )

        return {
            "order": order,
            "tracks": tracks
        }