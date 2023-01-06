from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from app.db.session import get_db
from app.core.config import settings
from app.models.user import User
from app.crud.user import user

JWT_SECRET_KEY = settings.JWT_SECRET_KEY
JWT_ALG = settings.JWT_ALG
JWT_EXP = settings.JWT_EXP

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_URL}/auth/login")


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User | None:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALG])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    current_user = user.get_by_email(db=db, email=email)
    if current_user is None:
        raise credentials_exception
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="User is not active")

    return current_user


def authenticate_user(db: Session, email: str, password: str) -> User | bool:
    auth_user = user.get_by_email(db=db, email=email)
    if auth_user is None:
        return False
    if not verify_password(password, auth_user.password):  # type: ignore
        return False
    return auth_user


def create_access_token(
    data: dict, expires_delta: timedelta | None = timedelta(minutes=JWT_EXP)
) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta  # type: ignore
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALG)
    return encoded_jwt
