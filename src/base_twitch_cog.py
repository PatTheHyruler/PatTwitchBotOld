from typing import TypeVar, TYPE_CHECKING, Generic

from twitchio.ext import commands
from twitchio.ext.commands.meta import CogMeta

from .service import BaseServiceUnitOfWork

if TYPE_CHECKING:
    from .twitch_bot import TwitchBot

TServiceUOW = TypeVar("TServiceUOW", bound=BaseServiceUnitOfWork)


class BaseTwitchCog(commands.Cog, Generic[TServiceUOW], metaclass=CogMeta):
    def __init__(self, bot: "TwitchBot", service_uow: TServiceUOW):
        print(self.__class__, "initialized")
        self.bot = bot
        self._service_uow = service_uow

    @staticmethod
    async def verify_mod(ctx: commands.Context) -> bool:
        if ctx.author.is_mod:
            return True
        await ctx.reply("You do not have permission to use this command!")
        return False
