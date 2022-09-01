import logging
from typing import TypeVar, TYPE_CHECKING

from twitchio.ext import commands

from .config import Config
from .service import BaseServiceUnitOfWork

_logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .twitch_bot import TwitchBot

TServiceUOW = TypeVar("TServiceUOW", bound=BaseServiceUnitOfWork)


class BaseBasicTwitchCog(commands.Cog):
    def __init__(self, bot: "TwitchBot"):
        self.bot = bot
        _logger.info(self.__class__, "initialized")

    @staticmethod
    async def verify_mod(ctx: commands.Context) -> bool:
        if ctx.author.is_mod:
            return True
        await ctx.reply("You do not have permission to use this command!")
        return False

    @staticmethod
    async def verify_owner(ctx: commands.Context) -> bool:
        if ctx.author.name in Config.get().Twitch.Owners:
            return True
        await ctx.reply("You do not have permission to use this command!")
        return False
