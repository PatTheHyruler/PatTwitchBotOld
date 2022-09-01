from src import BaseServiceUnitOfWork, TwitchBot
from .twitch_broadcaster_service import TwitchBroadcasterService
from .twitch_clip_service import TwitchClipService
from ..storage import StorageUnitOfWork


class ServiceUnitOfWork(BaseServiceUnitOfWork[StorageUnitOfWork]):
    def __init__(
        self, bot: TwitchBot, storage_uow: StorageUnitOfWork
    ):
        super().__init__(storage_uow)

        self.twitch_broadcasters = TwitchBroadcasterService(bot, storage_uow.twitch_broadcasters, storage_uow)
        self.twitch_clips = TwitchClipService(bot, storage_uow.twitch_clips, storage_uow)
