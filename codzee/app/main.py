from fastapi import FastAPI, HTTPException

from .db import get_conn, init_db
from .schemas import Task, TaskCreate

app = FastAPI(title="Taskly", version="0.1.0")
init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO tasks (title, description) VALUES (?, ?)",
            (payload.title, payload.description),
        )
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (cur.lastrowid,)).fetchone()
    return dict(row)


@app.get("/tasks", response_model=list[Task])
def list_tasks():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM tasks ORDER BY id").fetchall()
    return [dict(r) for r in rows]


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return dict(row)


@app.patch("/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: int):
    with get_conn() as conn:
        conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return dict(row)


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    with get_conn() as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
