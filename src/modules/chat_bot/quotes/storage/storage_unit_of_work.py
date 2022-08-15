from sqlalchemy.ext.asyncio import AsyncSession

from src import BaseStorageUnitOfWork
from .repository.quote_repository import QuoteRepository


class StorageUnitOfWork(BaseStorageUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

        self.quotes = QuoteRepository(self._session)
