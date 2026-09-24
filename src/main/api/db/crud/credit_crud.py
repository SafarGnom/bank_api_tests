from sqlalchemy.orm import Session
from src.main.api.db.models.credit_table import Credit


class CreditCrudDb:

    @staticmethod
    def get_credit_id(db: Session, credit_id: int) -> Credit | None:
        return (
            db.query(Credit)
            .filter(Credit.id == credit_id)
            .first()
        )
