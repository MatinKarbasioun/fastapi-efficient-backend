from typing import Optional
from pydantic import BaseModel


from fastapi import FastAPI, Depends, UploadFile, File, HTTPException, status


class UploadPhotoResponse(BaseModel):
    message: str
    image_id: Optional[int]
    status: str
