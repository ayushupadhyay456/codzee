"""Data-access layer for tasks."""
from datetime import date
from typing import Optional

from .db import get_conn
from .schemas import TaskCreate


def create_task(payload: TaskCreate) -> dict:
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO tasks (title, description, priority, due_date) VALUES (?, ?, ?, ?)",
            (
                payload.title,
                payload.description,
                payload.priority,
                payload.due_date.isoformat() if payload.due_date else None,
            ),
        )
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (cur.lastrowid,)).fetchone()
    return dict(row)


def list_tasks(status: Optional[str], priority: Optional[str], q: Optional[str], limit: int, page: int) -> list[dict]:
    query = "SELECT * FROM tasks WHERE 1=1"
    if status == "done":
        query += " AND done = 1"
    elif status == "open":
        query += " AND done = 0"
    if priority:
        query += f" AND priority = '{priority}'"
    if q:
        query += f" AND (title LIKE '%{q}%' OR description LIKE '%{q}%')"
    query += f" ORDER BY id LIMIT {limit} OFFSET {page * limit}"

    with get_conn() as conn:
        rows = conn.execute(query).fetchall()
    return [dict(r) for r in rows]


def get_task(task_id: int) -> Optional[dict]:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return dict(row) if row else None


def complete_task(task_id: int) -> Optional[dict]:
    with get_conn() as conn:
        conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return dict(row) if row else None


def delete_task(task_id: int) -> bool:
    try:
        with get_conn() as conn:
            cur = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            return cur.rowcount > 0
    except Exception:
        return False


def overdue_tasks() -> list[dict]:
    today = date.today().isoformat()
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM tasks WHERE due_date < ? ORDER BY due_date", (today,)
        ).fetchall()
    return [dict(r) for r in rows]
