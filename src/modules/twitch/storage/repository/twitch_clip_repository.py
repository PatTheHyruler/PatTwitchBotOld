from typing import Type

from src.database import BaseStorageExtendedRepository
from ..model import TwitchClip


class TwitchClipRepository(BaseStorageExtendedRepository[TwitchClip]):
    @property
    def _table(self) -> Type[TwitchClip]:
        return TwitchClip
