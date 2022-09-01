from typing import Type, Optional

from sqlalchemy import select

from src.database import BaseStorageExtendedRepository
from ..model.twitch_broadcaster import TwitchBroadcaster


class TwitchBroadcasterRepository(BaseStorageExtendedRepository[TwitchBroadcaster]):
    @property
    def _table(self) -> Type[TwitchBroadcaster]:
        return TwitchBroadcaster

    async def get_by_login(self, login: str) -> Optional[TwitchBroadcaster]:
        stmt = select(self._table).where(self._table.login == login)
        return await self._first(stmt)
