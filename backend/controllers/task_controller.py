from typing import Annotated

from fastapi import Depends, Request
from fastapi.routing import APIRouter
from starlette.templating import Jinja2Templates

from backend.dto.task_req import task_request
from backend.dto.task_req import  task_update_request

import backend.services.task_service as task_service
from backend.auth import get_current_user

api = APIRouter(prefix="/tasks")

templates = Jinja2Templates(directory="templates")

@api.get("/")
async def task_page(request: Request):
    return templates.TemplateResponse("task.html", {"request": request, "message": ""})

@api.post("/")
async def create_task(req: task_request, user_id:Annotated[str, Depends(get_current_user)]):
    return task_service.create_task(req, user_id)


@api.get("/view", )
async def get_all_task(user_id: Annotated[str, Depends(get_current_user)]):
    return task_service.view_task(user_id)


@api.patch("/{task_id}")
async def update_task(task_id : int, req : task_update_request, user_id:Annotated[str, Depends(get_current_user)]):
    return task_service.update_task(task_id, req, user_id)


@api.delete("/all")
async def delete_all_task(user_id:Annotated[str, Depends(get_current_user)]):
    return task_service.delete_all_task(user_id)


@api.delete("/{task_id}")
async def delete_task(task_id : int, user_id:Annotated[str, Depends(get_current_user)]):
    return task_service.delete_task(task_id, user_id)



