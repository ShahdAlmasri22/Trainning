from typing import Annotated
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates
from backend.dto.user_req import login as login_dto
from backend.dto.user_req import profile
from backend.dto.user_req import user_request
from backend.models.database import get_db
from backend.models.user import Role
from backend.services import user_service
from backend.auth import get_current_user, create_access_token


templates = Jinja2Templates(directory="templates")
api = APIRouter(prefix="/users") # every url start with users


@api.get("/")
async def get_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "message": ""})

@api.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "message": ""})

@api.get("/user_mang")
async def task_page(request: Request):
    return templates.TemplateResponse("userManagement.html", {"request": request, "message": ""})

@api.get("/view")
async def view_user(request: Request, user_id:Annotated[int, Depends(get_current_user)], session: Session = Depends(get_db)):
    return user_service.view_user(request, user_id, session)

@api.get("/search")
async def search_task(request:Request, key: str, user_id:Annotated[int, Depends(get_current_user)],session: Session = Depends(get_db)):
    return user_service.search_user(request, key, user_id, session)

@api.post("/")
async def create_user(request: Request, req: user_request, session: Session = Depends(get_db)):
        return user_service.create_user(request, req, session)


@api.post("/login")
async def login_user(request: Request, req: login_dto, session: Session = Depends(get_db)):
        return user_service.log_in(request, req, session)


@api.post("/refresh")
async def refresh(user_id_token:Annotated[int, Depends(get_current_user)] ):
   refresh_token = create_access_token(user_id_token)
   return {
       "access_token" : refresh_token
   }


@api.patch("/profile/{user_id}")
async def update_info(request: Request, req: profile, user_id : int, user_id_token:Annotated[int, Depends(get_current_user)], session: Session = Depends(get_db)):
    return user_service.update_info(request, req, user_id, user_id_token, session)

@api.delete("/{user_id}")
async def delete_account(request: Request, user_id : int, user_id_token:Annotated[int, Depends(get_current_user)],session: Session = Depends(get_db)):
    return user_service.delete_account(request, user_id, user_id_token, session)

@api.patch("/role/{user_id}")
async def update_role(request: Request, user_id : int, new_role: Role, user_id_token:Annotated[int, Depends(get_current_user)],session: Session = Depends(get_db)):
    return user_service.update_role(request, user_id, user_id_token, session, new_role)

