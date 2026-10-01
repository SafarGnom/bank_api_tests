from sqlalchemy.orm import Session

from src.main.api.db.models.user_table import User


class UserCrudDb:
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User | None:
        return db.query(User).filter_by(username=username).first()

    @staticmethod
    def create_account(db: Session, username: str, password: str, role: str) -> User:
        user = User(
            username=username,
            password=password,
            role=role
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> None:
        user = db.get(User, user_id)
        if user:
            db.delete(user)
            db.commit()
