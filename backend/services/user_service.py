from datetime import datetime, timedelta
from urllib.request import Request

from fastapi import HTTPException
from sqlalchemy import or_

from backend.dto.user_req import user_request, login, profile
from backend.auth import create_access_token, decode_token, create_refresh_token
from backend.models.user import User, Role
import hashlib

from backend.services import logged_service


def create_user(request, req: user_request, session):
    check_rate_limit(req.email)
    user_id = None
    existing_email= session.query(User).filter(User.email==req.email).first()
    if existing_email:
        logged_service.create_logged(method=request.method, path=request.url.path, status=409, user_id=None, session= session)

        raise HTTPException(
            status_code=409,
            detail=f"Email {req.email} is already in use"
        )


    hashed_password= hash_password(req.password)

    new_user = User(name=req.name, email=req.email, password=hashed_password, role=Role.USER.value)


    try:
        session.add(new_user)
        session.commit()
        new_user=session.query(User).filter(User.email==req.email).first()
        access_token = create_access_token(new_user.user_id)
        refresh_token = create_refresh_token(new_user.user_id)
        user_id = decode_token(access_token, request, session)
        role = new_user.role
        logged_service.create_logged(method=request.method, path=request.url.path, status=201, user_id=user_id, session= session)

        return {
            "status_code": 201,
            "message": "✅ User created successfully",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user_id,
            "role": role,
            "user": {
                "name": req.name,
                "email": req.email
            }
        }
    except Exception as e:
        session.rollback()
        logged_service.create_logged(method=request.method, path=request.url.path, status=500, user_id=user_id, session= session)

        raise HTTPException(
            status_code=500,
            detail=f"Error creating user: {str(e)}"
        )


login_attempts = {}
MAX_ATTEMPTS = 5
TIME_WINDOW = 60

def check_rate_limit(email: str):
    now = datetime.now()
    attempts = login_attempts.get(email, [])

    new_attempts = []

    for t in attempts:
        if now - t < timedelta(seconds=TIME_WINDOW):
            new_attempts.append(t)

    attempts = new_attempts

    login_attempts[email] = attempts

    if len(attempts) >= MAX_ATTEMPTS:
        raise HTTPException(
            status_code=429,
            detail="Too many request attempts. Try again later."
        )

    attempts.append(now)
    login_attempts[email] = attempts


def log_in(request, req: login, session):
    check_rate_limit(req.email)

    user=session.query(User).filter(User.email==req.email).first()
    if not user:
        logged_service.create_logged(method=request.method, path=request.url.path, status=404, user_id=None, session= session)

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    hashed_input = hash_password(req.password)

    if hashed_input == user.password:
        access_token = create_access_token(user.user_id)
        refresh_token = create_refresh_token(user.user_id)
        user_id = decode_token(access_token, request, session)

        logged_service.create_logged(method=request.method, path=request.url.path, status=200, user_id=user_id, session= session)
        return {
            "status_code": 200,
            "message": "✅ Login successfully",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user_id,
            "role": user.role.value
        }
    else:
        logged_service.create_logged(method=request.method, path=request.url.path, status=401, user_id=None, session= session)
        raise HTTPException(
            status_code=401,
            detail="Wrong password!"
        )


def update_info(request, req: profile, user_id : int, user_id_token: int, session):
    user = session.query(User).filter(User.user_id==user_id).first()

    if not user:
        logged_service.create_logged(method=request.method, path=request.url.path, status=404, user_id=None, session= session)
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    if user.user_id != user_id_token:
        logged_service.create_logged(method=request.method, path=request.url.path, status=403, user_id=user_id_token, session= session)
        raise HTTPException(
            status_code=403,
            detail="You don't have permission"
        )

    check_rate_limit(user.email)

    if req.name:
        user.name = req.name

    if req.new_password:
        if not req.old_password:
            logged_service.create_logged(method=request.method, path=request.url.path, status=404, user_id=user_id_token,
                                         session=session)
            raise HTTPException(
                status_code=404,
                detail="Old password required"
            )

        hashed_old = hash_password(req.old_password)

        if hashed_old == user.password:
            user.password = hash_password(req.new_password)

        else:
            logged_service.create_logged(method=request.method, path=request.url.path, status=403, user_id=user_id_token,
                                         session=session)

            raise HTTPException(
                status_code=403,
                detail="Wrong password"
            )

    try:
        session.commit()
        logged_service.create_logged(method=request.method, path=request.url.path, status=200, user_id=user_id_token, session= session)
        return {
            "status_code": 200,
            "message": "User info updated successfully",
        }
    except Exception as e:
        session.rollback()
        logged_service.create_logged(method=request.method, path=request.url.path, status=500, user_id=user_id_token, session= session)

        raise HTTPException(
            status_code=500,
            detail=f"Error updating user: {str(e)}"
        )

def hash_password(password: str):
    return hashlib.sha256(password.strip().encode('utf-8')).hexdigest()


def delete_account(request, user_id, user_id_token, session):
    user= session.query(User).filter(User.user_id == user_id).first()
    user_token = session.query(User).filter(User.user_id == user_id_token).first()
    if user is None:
        logged_service.create_logged(method=request.method, path=request.url.path, status=404, user_id=None, session= session)
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    if user.user_id != user_id_token:
        if(user_token.role != Role.ADMIN):
            logged_service.create_logged(method=request.method, path=request.url.path, status=403, user_id=user_id_token, session= session)
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to delete account"
            )
    try:
        session.delete(user)
        session.commit()
        logged_service.create_logged(method=request.method, path=request.url.path, status=200, user_id=user_id_token, session= session)

        return {
            "status_code": 200,
            "message": "User deleted successfully"
        }
    except Exception as e:
        session.rollback()
        logged_service.create_logged(method=request.method, path=request.url.path, status=500, user_id=user_id_token, session= session)

        raise HTTPException(
            status_code=500,
            detail="Error deleting user"
        )

def update_role(request, user_id, user_id_token, session, new_role):
    admin = session.query(User).filter(User.user_id==user_id_token).first()
    if not admin:
        logged_service.create_logged(method=request.method, path=request.url.path, status=404, user_id=None, session= session)
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    if admin.role != Role.ADMIN:
        logged_service.create_logged(method=request.method, path=request.url.path, status=403, user_id=user_id_token, session= session)
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to change role"
        )

    check_rate_limit(admin.email)
    user = session.query(User).filter(User.user_id==user_id).first()
    if not user:
        logged_service.create_logged(method=request.method, path=request.url.path, status=404, user_id=user_id_token, session= session)
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.role = new_role
    try:
        session.commit()
        logged_service.create_logged(method=request.method, path=request.url.path, status=200, user_id=user_id_token, session= session)
        return {
            "status_code": 200,
            "message": "User updated successfully"
        }
    except Exception as e:
        session.rollback()
        logged_service.create_logged(method=request.method, path=request.url.path, status=500, user_id=user_id_token, session= session)
        raise HTTPException(
            status_code=500,
            detail=f"Error updating user: {str(e)}"
        )

def view_user(request, user_id, session):
    user = session.query(User).filter(User.user_id==user_id).first()
    if not user:
        logged_service.create_logged(method=request.method, path=request.url.path, status=404, user_id=None, session= session)
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    if user.role != Role.ADMIN:
        logged_service.create_logged(method=request.method, path=request.url.path, status=403, user_id=user_id, session= session)

        raise HTTPException(
            status_code=403,
            detail="You don't have permission to view users"
        )

    users = session.query(User).all()
    all_users = []
    for u in users:
        all_users.append({
            "ID": u.user_id,
            "name": u.name,
            "email": u.email,
            "role": u.role,
        })

    logged_service.create_logged(method=request.method, path=request.url.path, status=200, user_id=user_id, session= session)
    return {
        "status_code": 200,
        "users": all_users
    }

def search_user(request:Request, key, user_id, session):

    user = session.query(User).filter(User.user_id==user_id).first()
    if not user:
        logged_service.create_logged(method=request.method, path=request.url.path, status=404, user_id=None,
                                     session=session)
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    if user.role != Role.ADMIN:
        logged_service.create_logged(method=request.method, path=request.url.path, status=403, user_id=user_id,
                                     session=session)

        raise HTTPException(
            status_code=403,
            detail="You don't have permission to search users"
        )

    matched_users = session.query(User).filter(
        or_(
            User.name.ilike(f'%{key}%'),
            User.role.ilike(f'%{key}%'),
            User.email.ilike(f'%{key}%'),
        )
    ).all()

    if not matched_users:
        logged_service.create_logged(method=request.method, path=request.url.path, status=404, user_id=user_id,
                                     session=session)
        return {
            "status_code": 404,
            "message": "No matching users found"
        }

    result = []
    for u in matched_users:
        result.append({
            "ID": u.user_id,
            "name": u.name,
            "email": u.email,
            "role": u.role,
        })


    logged_service.create_logged(method=request.method, path=request.url.path, status=200, user_id=user_id,
                                 session=session)
    return {
        "status_code": 200,
        "users": result,
    }