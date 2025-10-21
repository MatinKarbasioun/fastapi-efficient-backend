import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
import ray

from application.actors.image_processor import ImageProcessorActor
from settings import get_settings

from controllers.routers.photo import image_router


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """application lifespan event handler"""
    settings = get_settings()
    ray.init()
    ImageProcessorActor.options(
        name=settings.actor_name,
        get_if_exists=True
    ).remote()
    logger.info("Starting up...")

    yieldclear
    
    ray.shutdown()
    logger.info("Shutting down...")

app = FastAPI(lifespan=lifespan, docs_url='/swagger')

app.include_router(image_router, prefix='/images', tags=['images'])


@app.get("/")
async def root():
    """root endpoint to check application up and running"""
    return {"message": "Hello World"}



if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)