from sqlalchemy.orm import Session
from app.database.repository import LogisticsRepository


class OrderService:

    @staticmethod
    def get_order_detail(db: Session, order_no: str):

        return LogisticsRepository.get_order_detail(
            db=db,
            order_no=order_no
        )