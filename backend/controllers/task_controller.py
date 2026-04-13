from typing import Annotated
from fastapi import Depends, Request
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates
from backend.dto.task_req import task_request
from backend.dto.task_req import  task_update_request
import backend.services.task_service as task_service
from backend.auth import get_current_user
from backend.models.database import get_db
from backend.models.task import Status, Priority


api = APIRouter(prefix="/tasks")

templates = Jinja2Templates(directory="templates")


@api.get("/")
async def task_page(request: Request):
    return templates.TemplateResponse("task.html", {"request": request, "message": ""})



@api.post("/")
async def create_task(request : Request, req: task_request, user_id:Annotated[int, Depends(get_current_user)], session: Session = Depends(get_db)):
    return task_service.create_task(request, req, user_id, session)


@api.get("/view" )
# async def get_all_task(request:Request, user_id: Annotated[int, Depends(get_current_user)], session: Session = Depends(get_db),
#                        limit: int =10, skip: int =0,):
#     return task_service.view_task(request, user_id, session, limit, skip)
async def get_all_task(request:Request, user_id: Annotated[int, Depends(get_current_user)], session: Session = Depends(get_db)):
    return task_service.view_task(request, user_id, session)

@api.get("/view/status" )
async def filter_by_status(request:Request, status:Status, user_id: Annotated[int, Depends(get_current_user)], session: Session = Depends(get_db)):
    return task_service.filter_by_status(request, user_id, session, status)

@api.get("/view/priority" )
async def filter_by_priority(request:Request, priority:Priority, user_id: Annotated[int, Depends(get_current_user)], session: Session = Depends(get_db)):
    return task_service.filter_by_priority(request, user_id, session, priority)

@api.get("/filter")
async def get_tasks(
    request:Request,
    user_id: Annotated[int, Depends(get_current_user)], session: Session = Depends(get_db),
    sort_by: str = "created_at",
    order: str = "desc",
    skip: int | None = 0,
    limit: int | None = 10
):
    return task_service.get_tasks(request, user_id,session,sort_by,order,skip,limit)

# This is a comprehensive filter between Priority and States for frontend
@api.get("/prio_stat")
async def prio_stat(
    request:Request,
    user_id: Annotated[int, Depends(get_current_user)], session: Session = Depends(get_db),
    priority: Priority | None = None,
    status:Status | None = None,
):
    return task_service.prio_stat(request, user_id,session,priority,status)



@api.patch("/{task_id}")
async def update_task(request:Request, task_id : int, req : task_update_request, user_id:Annotated[int, Depends(get_current_user)], session: Session = Depends(get_db)):
    return task_service.update_task(request, task_id, req, user_id, session)


@api.delete("/all")
async def delete_all_task(request:Request, user_id:Annotated[int, Depends(get_current_user)], session: Session = Depends(get_db)):
    return task_service.delete_all_task(request, user_id, session)


@api.delete("/{task_id}")
async def delete_task(request:Request, task_id : int, user_id:Annotated[int, Depends(get_current_user)], session: Session = Depends(get_db)):
    return task_service.delete_task(request, task_id, user_id, session)


@api.get("/search")
async def search_task(request:Request, key: str, user_id:Annotated[int, Depends(get_current_user)],session: Session = Depends(get_db)):
    return task_service.search_task(request, key, user_id, session)

@api.get("/view_all_tasks")
async def view_all_tasks(request:Request, user_id:Annotated[int, Depends(get_current_user)],session: Session = Depends(get_db) ):
    return task_service.view_all_tasks(request, user_id, session)
