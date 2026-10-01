from sqlalchemy.orm import Session

from src.main.api.db.models.transaction_table import Transaction

class TransactionCrudDb:
    @staticmethod
    def get_amount(db: Session, amount: float) -> Transaction | None:
        return db.query(Transaction).filter(Transaction.amount == amount).first()

    @staticmethod
    def get_account_id(db: Session, account_id: float) -> Transaction | None:
        return db.query(Transaction).filter(Transaction.to_account_id == account_id).first()

    @staticmethod
    def delete_transaction(db: Session, transaction_id: int) -> None:
        transaction = db.get(Transaction, transaction_id)
        if transaction:
            db.delete(transaction)
            db.commit()

    @staticmethod
    def delete_transactions_by_account_id(
            db: Session,
            account_id: int
    ) -> None:
        transactions = db.query(Transaction).filter(
            Transaction.to_account_id == account_id
        ).all()

        for transaction in transactions:
            db.delete(transaction)

        db.commit()

