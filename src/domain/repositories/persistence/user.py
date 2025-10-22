from abc import ABC, abstractmethod
from typing import Optional, List

from fastapi_pagination import Page, Params
from fastapi_filter.contrib.sqlalchemy.filter import Filter

from domain.entities.user import User
from domain.value_objects import Ordering, SortField


class IUserRepository(ABC):

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_customer_id(self, customer_id: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def search(
            self,
            filters: Filter,
            page_params: Params,
            sorting: Optional[SortField]=None, 
            ordering: Optional[Ordering] = None
    ) -> Page[User]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, customer: User) -> User:
        raise NotImplementedError

    @abstractmethod
    async def remove(self, customer_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def is_exist(self, customer_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def update(self, user: User) -> User:
        raise NotImplementedError