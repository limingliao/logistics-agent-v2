"""
订单 Repository
"""

from sqlalchemy.orm import Session

from app.database.models import Order

from app.database.crud import OrderCRUD, TrackCRUD


class OrderRepository:

    @staticmethod
    def get_by_order_no(
        db: Session,
        order_no: str
    ) -> Order | None:
        return (
            db.query(Order)
            .filter(Order.order_no == order_no)
            .first()
        )

    @staticmethod
    def list_orders(
        db: Session,
        user_id: int
    ):
        return (
            db.query(Order)
            .filter(Order.user_id == user_id)
            .all()
        )

    @staticmethod
    def create(
        db: Session,
        order: Order
    ):
        db.add(order)
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def update_status(
        db: Session,
        order_no: str,
        status: str
    ):
        order = (
            db.query(Order)
            .filter(Order.order_no == order_no)
            .first()
        )

        if order:
            order.status = status
            db.commit()
            db.refresh(order)

        return order

