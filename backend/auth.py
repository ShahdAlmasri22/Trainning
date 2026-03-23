import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from fastapi import HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.models.database import get_db
from backend.services import logged_service

load_dotenv()
secret_key = os.getenv("SECRET_KEY")
alg = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user( request: Request, token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)):
    return decode_token(token, request, session)


def create_access_token(user_id: int):

    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
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


def decode_token(token: str, request, session):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[alg])
        user_id = payload.get("user_id")

        if user_id is None:
            logged_service.create_logged(method=request.method, path=request.url.path, status=401, user_id=None,
                                         session=session)
            raise HTTPException(
                status_code=401,
                detail="Invalid token payload"
            )

        return int(user_id)

    except jwt.ExpiredSignatureError:
        logged_service.create_logged(method=request.method, path=request.url.path, status=401, user_id=None,
                                     session=session)
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )

    except jwt.InvalidTokenError:
        logged_service.create_logged(method=request.method, path=request.url.path, status=401, user_id=None,
                                     session=session)
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

