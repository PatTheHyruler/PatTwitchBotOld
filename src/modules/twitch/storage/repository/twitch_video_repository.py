from typing import Type

from src.database import BaseStorageExtendedRepository
from ..model import TwitchVideo


class TwitchVideoRepository(BaseStorageExtendedRepository[TwitchVideo]):
    @property
    def _table(self) -> Type[TwitchVideo]:
        return TwitchVideo
