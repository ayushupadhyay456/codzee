# Taskly

A tiny task-management API built with FastAPI + SQLite.

## Run

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Docs at http://localhost:8000/docs

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | /health | Health check |
| POST | /tasks | Create a task |
| GET | /tasks | List tasks (`status`, `priority`, `q`, `limit`, `page`) |
| GET | /tasks/{id} | Get one task |
| PATCH | /tasks/{id}/complete | Mark done |
| DELETE | /tasks/{id} | Delete a task |
