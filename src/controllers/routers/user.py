from typing import Any, Dict
from fastapi import APIRouter, File, UploadFile, status
from starlette import status
import ray

from application.schemas.photo.upload import UploadPhotoResponse
from settings import get_settings


settings = get_settings()

user_router = APIRouter()


allowed_types = []


@user_router.post(
    "/users/{user_id}/profile-image",
    status_code=status.HTTP_202_ACCEPTED
)
async def start_batch_job() -> UploadPhotoResponse:
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


@user_router.get("/users/{user_id}/profile-image")
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

    