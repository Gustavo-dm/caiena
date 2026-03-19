from fastapi import APIRouter
from datetime import datetime,UTC

router = APIRouter()


@router.get("/")
async def index():

    return {
        "service": "weather-gist-api",
        "status": "running",
        "timestamp": datetime.now(UTC),
        "docs": "/docs",
        "endpoint": "/weather-comment"
    }