from typing import Annotated
from fastapi import APIRouter, Depends, Request
from starlette.responses import  JSONResponse
from starlette.templating import Jinja2Templates
from backend.dto.user_req import login as login_dto
from backend.dto.user_req import profile as  profile

from backend.dto.user_req import user_request
from backend.services import user_service as user_service
from backend.auth import get_current_user, create_access_token

templates = Jinja2Templates(directory="templates")
api = APIRouter(prefix="/users") # every url start with users


@api.get("/")
async def get_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "message": ""})

@api.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "message": "hhu"})


@api.post("/")
async def create_user(req: user_request):
    try:
        user_resp = user_service.create_user(req)
        return JSONResponse(status_code=201, content=user_resp)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"❌ {str(e)}"})


@api.post("/login")
async def login_user(req: login_dto):
    try:
        user =user_service.log_in(req)
        return JSONResponse(status_code=201, content=user)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"❌ {str(e)}"})

@api.post("/refresh")
async def refresh(user_id_token:Annotated[str, Depends(get_current_user)] ):
   refresh_token = create_access_token(user_id_token)
   return {
       "access_token" : refresh_token
   }


@api.patch("/profile/{user_id}")
async def update_info(req: profile, user_id : int, user_id_token:Annotated[str, Depends(get_current_user)] ):
    return user_service.update_info(req, user_id, user_id_token)

@api.delete("/{user_id}")
async def update_info(user_id : int, user_id_token:Annotated[str, Depends(get_current_user)] ):
    return user_service.delete_account(user_id, user_id_token)
