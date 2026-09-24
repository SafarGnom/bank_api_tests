from sqlalchemy.orm import Session

from src.main.api.db.models.transaction_table import Transaction

class TransactionCrudDb:
    @staticmethod
    def get_amount(db: Session, amount: float) -> Transaction | None:
        return db.query(Transaction).filter(Transaction.amount == amount).first()

    @staticmethod
    def get_account_id(db: Session, account_id: float) -> Transaction | None:
        return db.query(Transaction).filter(Transaction.to_account_id == account_id).first()

