from fastapi import APIRouter
from pydantic import File

file_router = APIRouter(prefix="/files", tags=["files"])



@file_router.post("/upload")
async def upload_photo(file:)