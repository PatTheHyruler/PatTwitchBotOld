from typing import Type

from src.database import BaseStorageRepository
from ..model.twitch_broadcaster import TwitchBroadcaster


class TwitchBroadcasterRepository(BaseStorageRepository[TwitchBroadcaster]):
    @property
    def _table(self) -> Type[TwitchBroadcaster]:
        return TwitchBroadcaster
