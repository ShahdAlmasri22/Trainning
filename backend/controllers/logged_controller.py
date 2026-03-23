from typing import Annotated

from fastapi import Depends, Request
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from backend.auth import get_current_user
from backend.models.database import get_db
from backend.services import logged_service

api = APIRouter(prefix="/logged")

templates = Jinja2Templates(directory="templates")


@api.get("/view")
async def view_logged(user_id:Annotated[str, Depends(get_current_user)], session: Session = Depends(get_db)):
    return logged_service.view_logged(user_id, session)

@api.get("/search")
async def view_logged(request:Request, key: str, user_id:Annotated[int, Depends(get_current_user)],session: Session = Depends(get_db)):
    return logged_service.search_log(request, key, user_id, session)
