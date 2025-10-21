from typing import Any, Dict
from fastapi import APIRouter
from starlette import status
import ray

from settings import get_settings


settings = get_settings()

image_router = APIRouter()


@image_router.post("/batch-process/start", status_code=status.HTTP_202_ACCEPTED)
async def start_batch_job():
    """
    Endpoint designated to batch image generation process
    """
    try:
        actor = ray.get_actor(settings.actor_name)
        
    except ValueError:
        return {"error": "Actor not found. App may be starting."}
    

    actor.process_batch.remote()
    
    return {
        "message": "Batch processing job started.",
        "actor_name": settings.actor_name
    }


@image_router.get("/batch-process/status")
async def get_batch_job_status() -> Dict[str, Any]:
    """
    Checks the status of the running batch job.
    """
    try:
        actor = ray.get_actor(settings.actor_name)
        
    except ValueError:
        return {"status": "NOT_STARTED", "detail": "Actor not found."}

    status = await actor.get_status.remote()
    return status

    