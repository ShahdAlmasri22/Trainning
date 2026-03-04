from pydantic import BaseModel

from backend.models.task import Status, Priority


class task_request(BaseModel):
    title : str
    description: str
    priority: Priority



class task_update_request(BaseModel):
    title : str | None = None
    description: str | None = None
    status :Status | None = None
    priority: Priority | None = None