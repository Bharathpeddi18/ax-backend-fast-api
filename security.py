import os
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError


import jwt
from dotenv import load_dotenv
from pwdlib import PasswordHash
load_dotenv()


JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


# Argon2 password hashing
password_hash = PasswordHash.recommended()

# region hash_password
def hash_password(password: str) -> str:
    return password_hash.hash(password)

# region verify_password 
def verify_password(plain_password: str, hashed_password: str, ) -> bool:
    return password_hash.verify(
        plain_password,
        hashed_password,
    )

# region Create JWT
def create_access_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)

    expire = now + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )

# region decode JWT
def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )

        return payload

    except InvalidTokenError:
        raise ValueError("Invalid or expired token")