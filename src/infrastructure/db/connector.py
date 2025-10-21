from fastapi import Depends

from sqlalchemy import create_engine

from src import get_settings

settings = get_settings()



class DbConnector:
    def __init__(self, db_url: str = Depends(get_settings.database_url)):
        self._engine = create_engine(db_url, echo=False, future=False)

    @property
    def engine(self):
        return self._engine

