"""
运费规则 Repository
"""

from sqlalchemy.orm import Session

from app.database.models import PriceRule


class PriceRepository:

    @staticmethod
    def get_price_rule(
        db: Session,
        origin: str,
        destination: str
    ) -> PriceRule | None:

        return (
            db.query(PriceRule)
            .filter(
                PriceRule.origin == origin,
                PriceRule.destination == destination
            )
            .first()
        )
