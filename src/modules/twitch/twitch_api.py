from typing import List

from src.base_twitch_cog import BaseTwitchCog
from .services import ServiceUnitOfWork
from .storage.model import TwitchBroadcaster


class TwitchAPI(BaseTwitchCog[ServiceUnitOfWork]):
    async def add_twitch_broadcaster(self, login: str = None, user_id: int = None) -> List[TwitchBroadcaster]:
        return await self._service_uow.twitch_broadcasters.add_twitch_broadcaster(login=login, user_id=user_id)
