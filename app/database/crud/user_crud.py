"""
用户 CRUD
"""

from sqlalchemy.orm import Session

from app.database.models import User


class UserCRUD:

    @staticmethod
    def get_by_phone(
        db: Session,
        phone: str
    ):

        return (
            db.query(User)
            .filter(
                User.phone == phone
            )
            .first()
        )

    @staticmethod
    def create(
        db: Session,
        user: User
    ):

        db.add(user)

        db.commit()

        db.refresh(user)

        return user