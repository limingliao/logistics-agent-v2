"""
ORM 数据模型
"""

# from sqlalchemy import String
# from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import mapped_column
#
from app.database.db import Base
#
#
# class Order(Base):
#     """
#     订单表
#     """
#
#     __tablename__ = "orders"
#
#     id: Mapped[int] = mapped_column(
#         primary_key=True,
#         autoincrement=True
#     )
#
#     order_no: Mapped[str] = mapped_column(
#         String(50),
#         unique=True,
#         index=True
#     )
#
#     sender: Mapped[str] = mapped_column(
#         String(50)
#     )
#
#     receiver: Mapped[str] = mapped_column(
#         String(50)
#     )
#
#     status: Mapped[str] = mapped_column(
#         String(30)
#     )
#
#     city: Mapped[str] = mapped_column(
#         String(50)
#     )
#
#     eta: Mapped[str] = mapped_column(
#         String(50)
#     )

from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]

    phone: Mapped[str]

    email: Mapped[str]

    orders = relationship(
        "Order",
        back_populates="user"
    )
from sqlalchemy import ForeignKey

class Order(Base):

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    order_no: Mapped[str]

    sender: Mapped[str]

    receiver: Mapped[str]
    # sender: Mapped[str] = mapped_column(String(50))
    # receiver: Mapped[str] = mapped_column(String(50))

    status: Mapped[str]

    city: Mapped[str]

    eta: Mapped[str]

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    user = relationship(
        "User",
        back_populates="orders"
    )

    tracks = relationship(
        "Track",
        back_populates="order"
    )
class Track(Base):

    __tablename__ = "tracks"

    id: Mapped[int] = mapped_column(primary_key=True)

    city: Mapped[str]

    remark: Mapped[str]

    track_time: Mapped[str]

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id")
    )

    order = relationship(
        "Order",
        back_populates="tracks"
    )