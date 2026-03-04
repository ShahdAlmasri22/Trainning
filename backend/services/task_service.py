from fastapi import HTTPException
from backend.dto.task_req import task_request, task_update_request
from backend.models.database import session
from backend.models.task import Task, Status



def create_task(req : task_request, user_id):
    new_task = Task(title=req.title,description= req.description,status= Status.PENDING,
                    priority= req.priority, user_id=user_id)

    try:
        session.add(new_task)
        session.commit()
        return {
            "statusCode": 201,
            "message": "✅ Task created successfully",
            "task": {
                "title": req.title,
                "priority": req.priority
            }
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error creating user: {str(e)}"
        )


def view_task(user_id):
    tasks = session.query(Task).filter(Task.user_id == user_id).all()

    if tasks is None:
        raise HTTPException(
            status_code=404,
            detail="There are no tasks"
        )

    result = []

    for task in tasks:
        result.append({
            "task_id": task.task_id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority
        })

    return result


def update_task(task_id: int , req : task_update_request, user_id:str):
    task=session.query(Task).filter(Task.task_id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    if task.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to update task"
        )
    if req.title:
        task.title = req.title
    if req.description:
        task.description = req.description
    if req.priority:
        task.priority = req.priority
    if req.status:
        task.status = req.status

    try:
       session.commit()
       return {
           "statusCode": 201,
           "message": "Task updated successfully"
       }
    except:
        raise HTTPException(
            status_code=500,
            detail="Error updating task"
        )


def delete_task(task_id, user_id):
    task=session.query(Task).filter(Task.task_id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    if task.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to delete task"
        )
    try:
        session.delete(task)
        session.commit()
        return {
            "statusCode": 201,
            "message": "Task deleted successfully"
            }
    except:
        raise HTTPException(
            status_code=500,
            detail="Error deleting task"
        )


def delete_all_task(user_id):
    tasks=session.query(Task).filter(Task.user_id == user_id).all()
    if tasks is None:
        raise HTTPException(
            status_code=404,
            detail="There are no tasks"
        )
    try:
        for task in tasks:
            session.delete(task)
            session.commit()
        return {
            "statusCode": 201,
            "message": "All tasks deleted successfully"
            }
    except:
        raise HTTPException(
            status_code=500,
            detail="Error deleting tasks"
        )


