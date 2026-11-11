from typing import Optional

from pydantic import EmailStr

from app.core.exception import (
    InvaildCredentialsException,
    MismatchPasswordException,
    UserAlreadyExistsException,
    UserNotFoundExeption,
)
from app.core.security import create_access_token, hash_password, verify_hash_password
from app.models.user import User
from app.repository.user_repository import UserRepository


class UserService:
    repository: Optional[UserRepository] = None

    def __init__(self, repository: Optional[UserRepository] = None):
        self.repository = repository or self.__class__.repository

    def register_user(self, email: EmailStr, password: str, conform_password: str) -> tuple[User, str]:
        if self.repository is None:
            raise ValueError("repository is required")

        if self.repository.user_exists(email):
            raise UserAlreadyExistsException()

        if password != conform_password:
            raise MismatchPasswordException()

        hash_pass = hash_password(password)
        new_user = self.repository.create_user(email, hash_pass)
        token = create_access_token(user_id=new_user.user_id)
        return new_user, token

    def login_user(self, email: str, password: str) -> tuple[User, str]:
        if self.repository is None:
            raise ValueError("repository is required")

        user = self.repository.get_user_with_email(email)
        if not user:
            raise UserNotFoundExeption()

        if not verify_hash_password(user.password_hash, password):
            raise InvaildCredentialsException()

        token = create_access_token(user_id=user.user_id)
        return user, token