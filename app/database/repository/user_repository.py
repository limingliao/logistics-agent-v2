"""
用户 Repository

负责组合 UserCRUD，
向 Service 提供用户数据。
"""

from sqlalchemy.orm import Session

from app.database.crud import UserCRUD
from app.database.models import User


class UserRepository:

    @staticmethod
    def get_by_phone(
        db: Session,
        phone: str
    ) -> User | None:
        """
        根据手机号查询用户
        """
        return UserCRUD.get_by_phone(
            db=db,
            phone=phone
        )

    @staticmethod
    def create_user(
        db: Session,
        user: User
    ) -> User:
        """
        创建用户
        """
        return UserCRUD.create(
            db=db,
            user=user
        )