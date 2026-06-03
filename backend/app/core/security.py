import hashlib
from datetime import datetime, timedelta
from typing import Optional, Union

import bcrypt
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from app.core.config import settings

ALGORITHM = "HS256"

# Token URLs
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
oauth2_scheme_refresh = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/refresh")

def _pre_hash(password: str) -> bytes:
    """
    Hash the password with SHA-256 to produce a 64-byte hex string,
    then encode to bytes for bcrypt (which expects a bytes input and has a 72-byte limit).
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest().encode("utf-8")

def create_access_token(subject: Union[str, int], expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(subject: Union[str, int], expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

def decode_refresh_token(token: str):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(_pre_hash(plain_password), hashed_password.encode("utf-8"))

def get_password_hash(password: str) -> str:
    # bcrypt.hashpw returns bytes; decode to string for storage
    return bcrypt.hashpw(_pre_hash(password), bcrypt.gensalt()).decode("utf-8")