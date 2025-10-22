import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import ray

from bootstrap import bootstrap

# from settings import get_settings

from controllers.routers import photo_router


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """application lifespan event handler"""
    bootstrap()
    logger.info("Starting up...")

    yield
    
    ray.shutdown()
    logger.info("Shutting down...")

app = FastAPI(lifespan=lifespan, docs_url='/swagger')

app.include_router(photo_router, prefix='/photo', tags=['images'])


@app.get("/")
async def root():
    """root endpoint to check application up and running"""
    return {"message": "Hello World"}



if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)