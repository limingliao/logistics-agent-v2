"""
订单 CRUD
"""

from sqlalchemy.orm import Session

from app.database.models import Order


class OrderCRUD:

    @staticmethod
    def get_by_order_no(
        db: Session,
        order_no: str
    ):

        return (
            db.query(Order)
            .filter(Order.order_no == order_no)
            .first()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        order_id: int
    ):

        return (
            db.query(Order)
            .filter(Order.id == order_id)
            .first()
        )

    @staticmethod
    def get_all(
        db: Session
    ):

        return db.query(Order).all()

    @staticmethod
    def create(
        db: Session,
        order: Order
    ):

        db.add(order)

        db.commit()

        db.refresh(order)

        return order