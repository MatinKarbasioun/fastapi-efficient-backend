from abc import ABC, abstractmethod


class IFileStorage(ABC):
    
    @abstractmethod
    async def save(cls, user_id: int, filename: str, content: bytes) -> str:
        """Saves file content, returns the storage URL/path."""
        raise NotImplementedError
