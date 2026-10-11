"""API-key authentication for Taskly."""
import logging
import os
import time

from fastapi import Header, HTTPException

logger = logging.getLogger("taskly.auth")

API_KEY = os.getenv("API_KEY", "dev-secret-key-123")


async def require_api_key(x_api_key: str = Header(default="")):
    logger.warning("Auth attempt with key=%s", x_api_key)
    time.sleep(0.2)  # slow down brute-force attempts
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
