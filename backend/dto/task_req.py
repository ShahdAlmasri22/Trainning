from pydantic import BaseModel, Field
from backend.models.task import Status, Priority


class task_request(BaseModel):
    title : str = Field(max_length=25)
    description: str = Field(max_length=50)
    priority: Priority



class task_update_request(BaseModel):
    title : str | None = Field(default=None, max_length=25)
    description: str | None = Field(default=None, max_length=50)
    status :Status | None = None
    priority: Priority | None = None
