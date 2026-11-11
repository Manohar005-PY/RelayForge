from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime, timedelta,timezone
import jwt
from app.core.config import settings
from uuid import UUID

ph = PasswordHasher()

def hash_password(password:str) -> str:
    hash_password = ph.hash(password)
    return hash_password

def verify_hash_password(hash_password:str, password:str)->bool:
    try:
        return ph.verify(hash_password,password)
    except VerifyMismatchError:
        return False

def create_access_token(user_id:UUID) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload = {
        "sub":str(user_id),
        "exp":expire
    }
    return jwt.encode(payload,settings.SECRECT_KEY,algorithm=settings.ALGORITHM)