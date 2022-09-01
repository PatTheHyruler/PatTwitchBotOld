from typing import Optional

from src import BaseService, TwitchBot
from ..storage import StorageUnitOfWork
from ..storage.model.quote import Quote
from ..storage.repository.quote_repository import QuoteRepository


class QuoteService(BaseService[Quote, QuoteRepository, StorageUnitOfWork]):
    def __init__(
            self,
            bot: TwitchBot,
            repository: QuoteRepository,
            storage_uow: StorageUnitOfWork,
    ):
        super().__init__(bot, repository, storage_uow)

    async def get_random_quote(self, context: str = None) -> Optional[Quote]:
        return await self.repository.get_random_quote(context=context)

    async def get_by_local_id(self, context: str, local_id: int) -> Optional[Quote]:
        return await self.repository.get_by_local_id(context, local_id)

    async def remove_by_local_id(self, context: str, local_id: int) -> Optional[Quote]:
        return await self.repository.remove_by_local_id(context, local_id)
