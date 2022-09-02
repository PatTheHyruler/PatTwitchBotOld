import datetime
import logging
from typing import List, Dict, Optional

from twitchio import Clip, PartialUser

from src import BaseService, TwitchBot
from ..storage import StorageUnitOfWork
from ..storage.model import TwitchVideo, TwitchBroadcaster
from ..storage.model.twitch_clip import TwitchClip
from ..storage.repository.twitch_clip_repository import TwitchClipRepository

_logger = logging.getLogger(__name__)


class TwitchClipService(BaseService[TwitchClip, TwitchClipRepository, StorageUnitOfWork]):
    def __init__(
            self,
            bot: TwitchBot,
            repository: TwitchClipRepository,
            storage_uow: StorageUnitOfWork,
    ):
        super().__init__(bot, repository, storage_uow)

    async def add_new_clips(self, clips: List[Clip], ended_at: datetime.datetime) -> List[TwitchClip]:
        broadcasters_proxy: Dict[int, TwitchBroadcaster] = {}

        async def get_broadcaster(user: PartialUser, mark_checked: bool = False) -> Optional[TwitchBroadcaster]:
            def should_update_checked_time(twitch_broadcaster: TwitchBroadcaster):
                return mark_checked and \
                       (twitch_broadcaster.last_checked is None or twitch_broadcaster.last_checked < ended_at)

            if user.id in broadcasters_proxy:
                twitch_broadcaster = broadcasters_proxy[user.id]
                if not should_update_checked_time(twitch_broadcaster):
                    return twitch_broadcaster
            async with self.bot.get_cog("TwitchAPI") as twitch:
                twitch_broadcaster = await twitch.add_twitch_broadcaster(user_id=user.id)
                if should_update_checked_time(twitch_broadcaster):
                    twitch_broadcaster.last_checked = ended_at
                broadcasters_proxy[user.id] = twitch_broadcaster
                return twitch_broadcaster

        added_clips: List[TwitchClip] = []

        for clip in clips:
            if not await self.storage_uow.twitch_clips.exists_external(clip.id):
                broadcaster = await get_broadcaster(clip.broadcaster, mark_checked=True)
                creator = await get_broadcaster(clip.creator)

                try:
                    video_id = int(clip.video_id)
                except ValueError:
                    pass
                else:
                    videos = await self.bot.fetch_videos(ids=[video_id])
                    if len(videos) == 1:
                        video = videos[0]
                        if not await self.storage_uow.twitch_videos.exists_external(video.id):
                            twitch_video = TwitchVideo(video)
                            twitch_video.authors.append(await get_broadcaster(video.user))
                            await self.storage_uow.twitch_videos.add(twitch_video)

                twitch_clip = TwitchClip(clip)
                twitch_clip.authors.append(creator)
                twitch_clip.authors.append(broadcaster)

                twitch_clip = await self.storage_uow.twitch_clips.add(twitch_clip)

                added_clips.append(twitch_clip)
        return added_clips
