from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from . import repository as repo
from .auth import require_api_key
from .db import init_db
from .schemas import Task, TaskCreate

app = FastAPI(title="Taskly", version="0.3.0", dependencies=[Depends(require_api_key)])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate):
    return repo.create_task(payload)


@app.get("/tasks", response_model=list[Task])
def list_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    q: Optional[str] = None,
    limit: int = 20,
    page: int = 1,
):
    """List tasks with optional filters, free-text search and pagination."""
    return repo.list_tasks(status, priority, q, limit, page)


# NOTE: must be declared before /tasks/{task_id} so "overdue" isn't parsed as an id
@app.get("/tasks/overdue", response_model=list[Task])
def overdue_tasks():
    """Tasks whose due date has passed."""
    return repo.overdue_tasks()


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = repo.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.patch("/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: int):
    task = repo.complete_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if not repo.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
