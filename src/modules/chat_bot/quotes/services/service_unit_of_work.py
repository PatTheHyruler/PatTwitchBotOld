from src import BaseServiceUnitOfWork, TwitchBot
from .quote_service import QuoteService
from ..storage import StorageUnitOfWork


class ServiceUnitOfWork(BaseServiceUnitOfWork[StorageUnitOfWork]):
    def __init__(
        self, bot: TwitchBot, storage_uow: StorageUnitOfWork
    ):
        super().__init__(storage_uow)

        self.quotes = QuoteService(bot, storage_uow.quotes, storage_uow)
