from typing import Generic, TypeVar, TYPE_CHECKING

from ..database.base_storage_unit_of_work import BaseStorageUnitOfWork

if TYPE_CHECKING:
    from ..twitch_bot import TwitchBot

TStorageUnitOfWork = TypeVar("TStorageUnitOfWork", bound=BaseStorageUnitOfWork)


class BaseBasicService(Generic[TStorageUnitOfWork]):
    def __init__(self, bot: "TwitchBot", storage_uow: TStorageUnitOfWork):
        self.bot = bot
        self.storage_uow = storage_uow
