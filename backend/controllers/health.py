from backend.auth import get_current_user
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy import text

from backend.models.database import engine, get_db
from backend.services import logged_service

api = APIRouter()

@api.get("/health")
async def health(request:Request, user_id:Annotated[int, Depends(get_current_user)],session: Session = Depends(get_db)):
    # this is to check the app
    status_report = {"app": "ok"}

    # to check DB
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            status_report["database"] = "ok"
    except Exception as e:
        logged_service.create_logged(method=request.method, path=request.url.path, status=500, user_id=user_id,
                                     session=session)
        status_report["database"] = f"error: {str(e)}"
        raise HTTPException(
            status_code=500,
            detail=status_report
        )

    return status_report