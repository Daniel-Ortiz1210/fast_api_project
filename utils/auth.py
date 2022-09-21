from datetime import timedelta, datetime

from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import jwt

from passlib.context import CryptContext

from config.models import UserTable
from config.db import session
from hashing_mod import bcrypt_context


SECRET_KEY = "TL6joGD7r4fBsbGBhXIVHNvphvFDZm42"
ALGORITHM = "HS256"

password_bearer = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verificar si la constraseña en texto plano y su version hashed conicidan

    Args:
        plain_password (str): Password en texto plano
        hashed_password (str): Password hasheada

    Returns:
        bool: Si coinciden, devolver True, en caso contrario, False 
    """
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(email: str, password: str, session: Session) -> UserTable:
    """

    Conprobaremos que el usuario exista y que la contraseña en texto plano coincida con su version hasheada.

    Args:
        email (str): Email del usuario
        password (str): Password en texto plano
        session (Session):

    Returns:
        UserTable: Devolvemos el usuario encontrado
    """
    user = session.query(UserTable).filter(UserTable.email == email).one_or_none()

    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    
    return user


def generate_access_token(email: str, id: int, expires:timedelta=None) -> jwt:
    
    encode = {"sub":email, "id":id}
    if expires:
        expire_time = datetime.utcnow() + expires
    else:
        expire_time = datetime.utcnow() + timedelta(minutes=15)
    
    encode.update({"exp":expire_time})
    
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)