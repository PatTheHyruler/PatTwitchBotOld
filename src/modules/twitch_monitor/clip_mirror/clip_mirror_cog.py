import datetime
import logging
from typing import Optional

from twitchio.ext import commands

from src import Config, BaseTwitchCog
from src.modules.twitch import ServiceUnitOfWork

_logger = logging.getLogger(__name__)


class ClipMirrorCog(BaseTwitchCog[ServiceUnitOfWork]):
    @commands.group(name="clip")
    async def clip(self, ctx: commands.Context):
        pass

    async def check_for_new_clips(self, full_check: bool = False):
        for login in Config.get().Download.Monitor.Clips:
            twitch_broadcaster = await self._service_uow.twitch_broadcasters.get_by_login(login)

            last_checked = None
            if twitch_broadcaster is not None and not full_check:
                last_checked = twitch_broadcaster.last_checked
            else:
                full_check = True

            ended_at = datetime.datetime.utcnow()
            channel = await self.bot.fetch_channel(login)
            limit = self._get_limit(full_check, last_checked, ended_at)

            clips = await channel.user.fetch_clips(started_at=last_checked, ended_at=ended_at, limit=limit)

            _logger.info(f"Fetched {len(clips)} clips from Twitch")

            if len(clips) == limit:
                if not full_check:
                    _logger.warning(
                        self.__class__,
                        f"Fetched clips length equals limit ({limit})! ({login=}, {limit=}, {last_checked=})"
                    )

            added_twitch_clips = await self._service_uow.twitch_clips.add_new_clips(clips)
            _logger.info(f"Added {len(added_twitch_clips)} clips for channel {login}!")
        await self._service_uow.save_changes()
        await self._service_uow.close()

    @staticmethod
    def _get_limit(
            full_check: bool,
            last_checked: Optional[datetime.datetime],
            ended_at: Optional[datetime.datetime]
    ) -> int:
        limit = 50
        if full_check:
            limit = 10000
        elif last_checked and ended_at:
            unchecked_period = ended_at - last_checked
            limit += unchecked_period.days * 10
        return limit

    @clip.command(name="check")
    async def clip_check(self, ctx: commands.Context):
        if not await self.verify_owner(ctx):
            return
        await self.check_for_new_clips()
