import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer


load_dotenv()
secret_key = os.getenv("SECRET_KEY")
alg = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    return decode_token(token)


def create_access_token(user_id: int):

    expire = datetime.now(timezone.utc) + timedelta(seconds=10)
    payload = {
        "user_id": user_id,
        "exp": expire
    }
    token = jwt.encode(payload, secret_key, algorithm=alg)
    return token

def create_refresh_token(user_id: int):

    expire = datetime.now(timezone.utc) + timedelta(days=7)
    payload = {
        "user_id": user_id,
        "exp": expire
    }
    token = jwt.encode(payload, secret_key, algorithm=alg)
    return token


def decode_token(token: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[alg])
        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token payload"
            )

        return user_id

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

