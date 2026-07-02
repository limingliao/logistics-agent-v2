"""
物流轨迹 CRUD
"""

from sqlalchemy.orm import Session

from app.database.models import Track


class TrackCRUD:

    @staticmethod
    def get_tracks(
        db: Session,
        order_id: int
    ):

        return (
            db.query(Track)
            .filter(
                Track.order_id == order_id
            )
            .all()
        )

    @staticmethod
    def create(
        db: Session,
        track: Track
    ):

        db.add(track)

        db.commit()

        db.refresh(track)

        return track