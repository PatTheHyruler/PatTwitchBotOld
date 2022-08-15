from sqlalchemy.ext.asyncio import AsyncSession

from src import BaseStorageUnitOfWork
from .repository.twitch_broadcaster_repository import TwitchBroadcasterRepository


class StorageUnitOfWork(BaseStorageUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

        self.twitch_broadcasters = TwitchBroadcasterRepository(self._session)
