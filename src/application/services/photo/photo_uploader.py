
from fastapi import Depends, File, HTTPException, UploadFile


class PhotoUploader:
    def __init__(self, user_repo: IUserRepository)
        self._user_repo = user_repo
        
    async def handle_upload_request(
        user_id: int,
        db: AsyncSession,
    ):
        """Handles the HTTP request for uploading a profile image."""
        try:
            content = await file.read()
            # Basic validation
            if not content:
                raise HTTPException(status_code=400, detail="Empty file uploaded.")
            if file.content_type not in ["image/jpeg", "image/png"]:
                raise HTTPException(status_code=415, detail="Unsupported file type.")

            # Use a transaction for the database operations
            async with db.begin(): # Manages commit/rollback via repository session
                # Call the application service to perform the use case
                new_image = await upload_service.upload_photo(
                    user_id=user_id,
                    filename=file.filename,
                    content=content
                )

            return UploadResponseSchema(
                message="Image uploaded, processing started.",
                image_id=new_image.id,
                status=new_image.status.value
            )

        except ValueError as e: # Catch domain errors (like User not found)
            # No rollback needed if db.begin() context manager exits with exception
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            # Catch infrastructure or unexpected errors
            # No rollback needed if db.begin() context manager exits with exception
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {e}")