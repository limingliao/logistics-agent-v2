"""
订单表
"""

from sqlalchemy import String
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.db import Base


class Order(Base):

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    order_no: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True
    )

    sender: Mapped[str] = mapped_column(
        String(50)
    )

    receiver: Mapped[str] = mapped_column(
        String(50)
    )

    status: Mapped[str] = mapped_column(
        String(30)
    )

    city: Mapped[str] = mapped_column(
        String(50)
    )

    eta: Mapped[str] = mapped_column(
        String(50)
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    user = relationship(
        "User",
        back_populates="orders"
    )

    tracks = relationship(
        "Track",
        back_populates="order",
        cascade="all, delete-orphan"
    )