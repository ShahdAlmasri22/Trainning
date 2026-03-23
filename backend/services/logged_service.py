from urllib.request import Request

from fastapi import HTTPException

from sqlalchemy import or_
from backend.models.logged import Logged
from backend.models.user import User, Role


def create_logged(method, path, status, user_id, session):
    log = Logged(method = method, path = path, status = status, user_id = user_id)
    try:
        session.add(log)
        session.commit()
        return {
            "status" : 201,
            "message" : "Logged saved Successfully",
        }

    except Exception as e:
        session.rollback()
        return {
            "status" : 500,
            "message" : str(e),
        }


def view_logged(user_id, session):
    user = session.query(User).filter(User.user_id == user_id).first()
    if not user:
        create_logged(method="Get", path="logged/view", status=404, user_id=None, session= session)
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    if user.role != Role.ADMIN:
        create_logged(method="Get", path="logged/view", status=403, user_id=None, session= session)
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to view logged"
        )
    try:
        logs = (
            session.query(Logged, User.email)
            .join(User, Logged.user_id == User.user_id, isouter=True)
            .all()
        )

        result = []

        for log, email in logs:
            result.append({
                "id": log.logged_id,
                "method": log.method,
                "path": log.path,
                "status": log.status,
                "user": email,
                "date": log.created_at.strftime("%Y-%m-%d %H:%M:%S") if log.created_at else None
            })

        create_logged(method="Get", path="logged/view", status=200, user_id=user_id, session=session)
        return {
            "status_code": 200,
            "result": result
        }

    except Exception as e:
        session.rollback()
        create_logged(method="Get", path="logged/view", status=500, user_id=user_id, session=session)
        return {
            "status": 500,
            "message": str(e),
        }


def search_log(request: Request, key: str, user_id: int, session):
    matched_logs = (
        session.query(Logged, User.email)
        .join(User, Logged.user_id == User.user_id, isouter=True)
        .filter(
            or_(
                Logged.method.ilike(f"%{key}%"),
                Logged.path.ilike(f"%{key}%"),
                Logged.status.ilike(f"%{key}%"),
                User.email.ilike(f"%{key}%")
            )
        )
        .all()
    )

    if not matched_logs:
        create_logged(
            method=request.method,
            path=request.url.path,
            status=404,
            user_id=user_id,
            session=session
        )
        return {
            "status_code": 404,
            "message": "No matching logs found"
        }

    result = []
    for log, email in matched_logs:
        result.append({
            "id": log.logged_id,
            "method": log.method,
            "path": log.path,
            "status": log.status,
            "user": email,
            "date": log.created_at.strftime("%Y-%m-%d %H:%M:%S") if log.created_at else None
        })

    create_logged(
        method=request.method,
        path=request.url.path,
        status=200,
        user_id=user_id,
        session=session
    )
    return {
        "status_code": 200,
        "result": result
    }