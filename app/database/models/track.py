"""
物流轨迹表
"""

from sqlalchemy import String
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.db import Base


class Track(Base):

    __tablename__ = "tracks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    city: Mapped[str] = mapped_column(
        String(50)
    )

    remark: Mapped[str] = mapped_column(
        String(200)
    )

    track_time: Mapped[str] = mapped_column(
        String(50)
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id")
    )

    order = relationship(
        "Order",
        back_populates="tracks"
    )