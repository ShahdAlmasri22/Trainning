from fastapi import HTTPException, Request
from sqlalchemy import case, or_
from backend.dto.task_req import task_request, task_update_request
from backend.models.task import Task, Status
from backend.models.user import User, Role
from backend.services import logged_service
from backend.services.user_service import check_rate_limit


def create_task(request:Request, req : task_request, user_id, session):
    user=session.query(User).filter(User.user_id == user_id).first()
    if user is None:
        logged_service.create_logged(method=request.method, path=request.url.path, status=404, user_id=None, session= session)
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    check_rate_limit(user.email)
    new_task = Task(title=req.title,description= req.description,status= Status.PENDING,
                    priority= req.priority, user_id=user_id)

    try:
        session.add(new_task)
        session.commit()
        logged_service.create_logged(method=request.method, path=request.url.path, status=201, user_id=user_id, session= session)

        return {
            "status_code": 201,
            "message": "✅ Task created successfully",
            "task": task_to_dict(new_task)
        }
    except Exception as e:
        session.rollback()
        logged_service.create_logged(method=request.method, path=request.url.path, status=500, user_id=user_id, session= session)
        raise HTTPException(
            status_code=500,
            detail=f"Error creating task: {str(e)}"
        )

def view_task(request:Request, user_id, session):
    #def view_task(request: Request, user_id, session, limit: int = 10, skip: int = 0):

    # tasks = session.query(Task).filter(Task.user_id == user_id).offset(skip).limit(limit).all()
    tasks = session.query(Task).filter(Task.user_id == user_id).all()

    total_tasks= session.query(Task).filter(Task.user_id == user_id).count()

    result = []

    for task in tasks:
        result.append(task_to_dict(task))

    logged_service.create_logged(method=request.method, path=request.url.path, status=200, user_id=user_id, session=session)

    return {
        "status_code": 200,
        "total_tasks": total_tasks,
        "tasks": result
    }

def filter_by_status(request:Request, user_id, session, status):
    taskss = session.query(Task).filter(Task.user_id == user_id , Task.status == status).all()
    if not taskss:
        logged_service.create_logged(method=request.method, path=request.url.path, status=404, user_id=user_id, session=session)
        raise HTTPException(
            status_code=404,
            detail="There are no tasks"
        )
    result = []

    for task in taskss:
        result.append(task_to_dict(task))

    logged_service.create_logged(method=request.method, path=request.url.path, status=200, user_id=user_id, session=session)
    return {
        "status_code": 200,
        "tasks": result
    }

def filter_by_priority(request:Request, user_id, session, priority):
    tasks = session.query(Task).filter(Task.user_id == user_id , Task.priority == priority).all()
    if not tasks:
        logged_service.create_logged(method=request.method, path=request.url.path, status=404, user_id=user_id, session=session)
        raise HTTPException(
            status_code=404,
            detail="There are no tasks"
        )
    result = []

    for task in tasks:
        result.append(task_to_dict(task))

    logged_service.create_logged(method=request.method, path=request.url.path, status=200, user_id=user_id, session=session)
    return {
        "status_code": 200,
        "tasks": result
    }


def get_tasks(request:Request, user_id, session, sort_by="created_at", order="desc", skip=0, limit=10):

    allowed_sort = ["created_at", "priority", "status", "title"]


    if sort_by not in allowed_sort:
        logged_service.create_logged(method=request.method, path=request.url.path, status=422, user_id=user_id, session=session)
        raise HTTPException(
            status_code=422,
            detail=f"Invalid sort_by field, input should be {allowed_sort}"
        )

    if order.lower() not in ["asc", "desc"]:
        logged_service.create_logged(method=request.method, path=request.url.path, status=422, user_id=user_id,
                                     session=session)
        raise HTTPException(
            status_code=422,
            detail="Invalid sort_by field, input should be \"asc\", \"desc\""
        )


    query = session.query(Task).filter(Task.user_id == user_id)
    tatal_task = query.count()

    if sort_by == "priority":
        column = case(
    (Task.priority == "LOW", 1),
            (Task.priority == "MEDIUM", 2),
            (Task.priority == "HIGH", 3)
        )

    elif sort_by == "status":
        column = case(
    (Task.status == "PENDING", 1),
            (Task.status == "RUNNING", 2),
            (Task.status == "COMPLETED", 3)
        )

    else:
        column = getattr(Task, sort_by)

    if order.lower() == "desc":
        query = query.order_by(column.desc())
    else:
        query = query.order_by(column.asc())

    total = query.count()

    tasks = query.offset(skip).limit(limit).all()

    result = []

    for task in tasks:
        result.append(task_to_dict(task))

    logged_service.create_logged(method=request.method, path=request.url.path, status=200, user_id=user_id, session=session)
    return {
        "status_code": 200,
        "total": total,
        "tasks": result,
        "total_tasks": tatal_task
    }


def update_task(request:Request, task_id: int , req : task_update_request, user_id, session):
    user = session.query(User).filter(User.user_id == user_id).first()
    if user is None:
        logged_service.create_logged(method=request.method, path=request.url.path, status=404, user_id=user_id,
                                     session=session)
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    check_rate_limit(user.email)

    task=session.query(Task).filter(Task.task_id == task_id).first()
    if task is None:
        logged_service.create_logged(method=request.method, path=request.url.path, status=404, user_id=user_id,
                                     session=session)
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    if task.user_id != user_id:
        logged_service.create_logged(method=request.method, path=request.url.path, status=403, user_id=user_id,
                                     session=session)
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to update task"
        )

    if req.title is not None:
        task.title = req.title

    if req.description is not None:
        task.description = req.description

    if req.priority is not None:
        task.priority = req.priority

    if req.status is not None:
        task.status = req.status

    try:
       session.commit()
       logged_service.create_logged(method=request.method, path=request.url.path, status=200, user_id=user_id,
                                    session=session)
       return {
           "status_code": 200,
           "message": "Task updated successfully"
       }
    except Exception as e:
        session.rollback()
        logged_service.create_logged(method=request.method, path=request.url.path, status=500, user_id=user_id,
                                     session=session)
        raise HTTPException(
            status_code=500,
            detail="Error updating task"
        )


def delete_task(request:Request, task_id, user_id, session):
    task=session.query(Task).filter(Task.task_id == task_id).first()
    if task is None:
        logged_service.create_logged(method=request.method, path=request.url.path, status=404, user_id=user_id,
                                     session=session)
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    if task.user_id != user_id:
        logged_service.create_logged(method=request.method, path=request.url.path, status=403, user_id=user_id,
                                     session=session)
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to delete task"
        )
    try:
        session.delete(task)
        session.commit()
        logged_service.create_logged(method=request.method, path=request.url.path, status=200, user_id=user_id,
                                     session=session)
        return {
            "status_code": 200,
            "message": "Task deleted successfully"
            }
    except Exception as e:
        session.rollback()
        logged_service.create_logged(method=request.method, path=request.url.path, status=500, user_id=user_id,
                                     session=session)
        raise HTTPException(
            status_code=500,
            detail="Error deleting task"
        )


def delete_all_task(request:Request, user_id, session):
    tasks=session.query(Task).filter(Task.user_id == user_id).all()
    if not tasks:
        logged_service.create_logged(method=request.method, path=request.url.path, status=404, user_id=user_id,
                                     session=session)
        raise HTTPException(
            status_code=404,
            detail="There are no tasks"
        )
    try:
        for task in tasks:
            session.delete(task)
        session.commit()
        logged_service.create_logged(method=request.method, path=request.url.path, status=200, user_id=user_id,
                                     session=session)
        return {
            "status_code": 200,
            "message": "All tasks deleted successfully"
            }
    except Exception as e:
        session.rollback()
        logged_service.create_logged(method=request.method, path=request.url.path, status=500, user_id=user_id,
                                     session=session)
        raise HTTPException(
            status_code=500,
            detail="Error deleting tasks"
        )


def task_to_dict(task):
    return {
        "task_id": task.task_id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
        "created_at": task.created_at,
        "updated_at": task.updated_at
    }


def search_task(request:Request, key, user_id, session):

    matched_tasks = session.query(Task).filter(
        Task.user_id == user_id,
        or_(
            Task.title.ilike(f'%{key}%'),
            Task.description.ilike(f'%{key}%'),
            Task.status.ilike(f'%{key}%'),
            Task.priority.ilike(f'%{key}%')
        )
    ).all()

    if not matched_tasks:
        logged_service.create_logged(method=request.method, path=request.url.path, status=404, user_id=user_id,
                                     session=session)
        return {
            "status_code": 404,
            "message": "No matching tasks found"
        }

    result = []
    for task in matched_tasks:
        result.append(task_to_dict(task))

    query = session.query(Task).filter(Task.user_id == user_id)
    tatal_task = query.count()

    logged_service.create_logged(method=request.method, path=request.url.path, status=200, user_id=user_id,
                                 session=session)
    return {
        "status_code": 200,
        "tasks": result,
        "total_tasks": tatal_task
    }

def view_all_tasks(request:Request, user_id, session):
    user=session.query(User).filter(User.user_id == user_id).first()
    if user is None:
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
            detail="You don't have permission to view tasks"
        )

    tasks=session.query(Task).all()
    if not tasks:
        logged_service.create_logged(method=request.method, path=request.url.path, status=404, user_id=user_id,
                                     session=session)
        raise HTTPException(
            status_code=404,
            detail="No tasks found"
        )

    result = []
    for task in tasks:
        task_user = session.query(User).filter(User.user_id == task.user_id).first()
        result.append({
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
            "user":task_user.email,
        })

    logged_service.create_logged(method=request.method, path=request.url.path, status=200, user_id=user_id,
                                 session=session)
    return {
        "status_code": 200,
        "tasks": result
    }


def prio_stat(request, user_id,session,priority,status):
    if priority is not None and status is not None:
        tasks = session.query(Task).filter(Task.user_id == user_id, Task.status == status, Task.priority == priority).all()

    elif priority is not None:
        tasks = session.query(Task).filter(Task.user_id == user_id, Task.priority == priority).all()

    elif status is not None:
        tasks = session.query(Task).filter(Task.user_id == user_id, Task.status == status).all()

    else:
        logged_service.create_logged(method=request.method, path=request.url.path, status=400, user_id=user_id,
                                     session=session)
        raise HTTPException(
            status_code=400,
            detail="Invalid value"
        )

    result = []

    for task in tasks:
        result.append(task_to_dict(task))

    tatal_task = session.query(Task).filter(Task.user_id == user_id).count()

    logged_service.create_logged(method=request.method, path=request.url.path, status=200, user_id=user_id,
                                 session=session)
    return {
        "status_code": 200,
        "tasks": result,
        "total_tasks": tatal_task
    }




