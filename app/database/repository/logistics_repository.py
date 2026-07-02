"""
物流 Repository
"""

from sqlalchemy.orm import Session

from app.database.models.logistics import Logistics

from app.database.crud import OrderCRUD


class LogisticsRepository:

    @staticmethod
    def get_track(
        db: Session,
        order_no: str
    ) -> Logistics | None:

        return (
            db.query(Logistics)
            .filter(Logistics.order_no == order_no)
            .first()
        )

    @staticmethod
    def get_history(
        db: Session,
        order_no: str
    ):

        return (
            db.query(Logistics)
            .filter(Logistics.order_no == order_no)
            .order_by(Logistics.create_time.desc())
            .all()
        )

    @staticmethod
    def save(
        db: Session,
        logistics: Logistics
    ):
        db.add(logistics)
        db.commit()
        db.refresh(logistics)

        return logistics

