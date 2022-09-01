from sqlalchemy.ext.asyncio import AsyncSession

from src.database import BaseStorageUnitOfWork
from .repository.twitch_broadcaster_repository import TwitchBroadcasterRepository
from .repository.twitch_clip_repository import TwitchClipRepository
from .repository.twitch_video_repository import TwitchVideoRepository


class StorageUnitOfWork(BaseStorageUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

        self.twitch_broadcasters = TwitchBroadcasterRepository(self._session)
        self.twitch_clips = TwitchClipRepository(self._session)
        self.twitch_videos = TwitchVideoRepository(self._session)
