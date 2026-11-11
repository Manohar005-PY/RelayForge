from app.db.session import get_db
from sqlalchemy.orm import Session
from app.models.user import User
from sqlalchemy import select, exists


class UserRepository:
    def __init__(self, db:Session):
        self.db = db

    def create_user(self,email,password_hash:str) -> User:
        new_user = User(email=email,password_hash=password_hash)
        self.db.add(new_user)
        self.db.flush()
        self.db.refresh(new_user)
        return new_user

    def user_exists(self,email) -> bool | None:
        stmt = select(exists().where(User.email == email))
        return self.db.scalar(stmt)

    def get_user_with_email(self,email) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.db.scalar(stmt)