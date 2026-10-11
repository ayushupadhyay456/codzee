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
| GET | /tasks/overdue | Tasks past their due date |
| PATCH | /tasks/{id}/complete | Mark done |
| DELETE | /tasks/{id} | Delete a task |

## Authentication

All endpoints require an `X-API-Key` header. Set the key with the `API_KEY` environment variable.

```bash
curl -H "X-API-Key: $API_KEY" http://localhost:8000/tasks
```
