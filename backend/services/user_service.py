from fastapi import HTTPException
from backend.dto.user_req import user_request, login, profile
from backend.auth import create_access_token, decode_token, create_refresh_token
from backend.models.user import User
import hashlib

def create_user(req: user_request, session):
    existing_email= session.query(User).filter(User.email==req.email).first()
    if existing_email:
        raise HTTPException(
            status_code=409,
            detail=f"Email {req.email} is already in use"
        )


    hashed_password= hash_password(req.password)

    new_user = User(name=req.name, email=req.email, password=hashed_password)


    try:
        session.add(new_user)
        session.commit()
        new_user=session.query(User).filter(User.email==req.email).first()
        access_token = create_access_token(new_user.user_id)
        refresh_token = create_refresh_token(new_user.user_id)
        user_id = decode_token(access_token)

        return {
            "statusCode": 201,
            "message": "✅ User created successfully",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user_id,
            "user": {
                "name": req.name,
                "email": req.email
            }
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error creating user: {str(e)}"
        )


def log_in(req: login, session):
    user=session.query(User).filter(User.email==req.email).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    hashed_input = hash_password(req.password)

    if hashed_input == user.password:
        access_token = create_access_token(user.user_id)
        refresh_token = create_refresh_token(user.user_id)
        user_id = decode_token(access_token)
        return {
            "message": "✅ Login successfully",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user_id
        }
    else:
        raise HTTPException(
            status_code=400,
            detail="Wrong password!"
        )


def update_info(req: profile, user_id : int, user_id_token: str, session):
    user = session.query(User).filter(User.user_id==user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    if user.user_id != user_id_token:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission"
        )
    if req.name:
        user.name = req.name

    if req.new_password:
        if not req.old_password:
            raise HTTPException(
                status_code=404,
                detail="Old password required"
            )

        hashed_old = hash_password(req.old_password)

        if hashed_old == user.password:
            user.password = hash_password(req.new_password)

        else:
            raise HTTPException(
                status_code=403,
                detail="Wrong password"
            )

    try:
        session.commit()
        return {
            "statusCode": 200,
            "message": "User info updated successfully",
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error updating user: {str(e)}"
        )

def hash_password(password: str):
    return hashlib.sha256(password.strip().encode('utf-8')).hexdigest()


def delete_account(user_id, user_id_token, session):
    user= session.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    if user.user_id != user_id_token:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to delete account"
        )
    try:
        session.delete(user)
        session.commit()
        return {
            "statusCode": 201,
            "message": "User deleted successfully"
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error deleting user"
        )
