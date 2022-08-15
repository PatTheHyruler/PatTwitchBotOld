from twitchio.ext import routines

from .clip_mirror_cog import ClipMirrorCog


class Routines:
    def __init__(self, clip_mirror_cog: ClipMirrorCog):
        self.clip_mirror_cog = clip_mirror_cog

    @routines.routine(hours=12)
    async def check_for_new_clips(self):
        await self.clip_mirror_cog.check_for_new_clips()

    @routines.routine(hours=12)
    async def start_downloading_new_clips(self):
        pass
