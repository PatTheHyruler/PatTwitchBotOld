from twitchio.ext import commands

from src.base_twitch_cog import BaseTwitchCog
from .services import ServiceUnitOfWork


class ClipMirrorCog(BaseTwitchCog[ServiceUnitOfWork]):
    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f"Hello, {ctx.author.name}")
        twitch_broadcaster = await self._service_uow.twitch_broadcasters.add_twitch_broadcaster(ctx.author.name)
        await self._service_uow.save_changes()
        await self._service_uow.refresh(twitch_broadcaster)
        await ctx.send(f"Hello, DB {twitch_broadcaster.display_name}")
        await self._service_uow.close()

    async def check_for_new_clips(self):
        pass
        # channel = await self.bot.fetch_channel("patthehyruler")
        # clips = await channel.user.fetch_clips()
        # for clip in clips:
        #     self.clip_download_queue.append(clip)

    @commands.command()
    async def clip_check(self, ctx: commands.Context):
        await self.check_for_new_clips()
