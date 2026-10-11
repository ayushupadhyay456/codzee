from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, Field

Priority = Literal["low", "medium", "high"]


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str = ""
    priority: Priority = "medium"
    due_date: Optional[date] = None


class Task(BaseModel):
    id: int
    title: str
    description: str
    done: bool
    priority: Priority
    due_date: Optional[str] = None
    created_at: str
