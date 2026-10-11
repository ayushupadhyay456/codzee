from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str = ""


class Task(BaseModel):
    id: int
    title: str
    description: str
    done: bool
    created_at: str
