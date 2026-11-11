from app.core.security import hash_password, verify_hash_password
from pydantic import EmailStr
from app.models.user import User
from app.repository.user_repository import UserRepository
from app.core.exception import MismatchPasswordException,UserAlreadyExistsException,InvaildCredentialsException,UserNotFoundExeption
from app.core.security import create_access_token


class UserService():
    def __init__(self,repository:UserRepository):
        self.repository = repository

    def register_user(self,email:EmailStr, password, conform_passowrd) -> tuple[User,str]:
        if self.repository.user_exists:
            raise UserAlreadyExistsException
        
        hash_pass = hash_password(password)
        if verify_hash_password(password, conform_passowrd):
            new_user = self.repository.create_user(email, hash_pass)
            token = create_access_token(user_id=new_user.user_id)
            return new_user, token
        else: 
            raise MismatchPasswordException

    def login_user(self,email,password:str) -> tuple[User, str]:
        user = self.repository.get_user_with_email(email)
        if not user:
            raise UserNotFoundExeption

        if not verify_hash_password(user.password_hash,password):
            raise InvaildCredentialsException
        

        token = create_access_token(user_id=user.user_id)
        return user,token