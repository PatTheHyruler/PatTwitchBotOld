from typing import TypeVar, TYPE_CHECKING, Generic

from twitchio.ext.commands.meta import CogMeta

from .base_basic_twitch_cog import BaseBasicTwitchCog
from .service import BaseServiceUnitOfWork

if TYPE_CHECKING:
    from .twitch_bot import TwitchBot

TServiceUOW = TypeVar("TServiceUOW", bound=BaseServiceUnitOfWork)


class BaseTwitchCog(BaseBasicTwitchCog, Generic[TServiceUOW], metaclass=CogMeta):
    def __init__(self, bot: "TwitchBot", service_uow: TServiceUOW):
        self._service_uow = service_uow
        super().__init__(bot)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._service_uow.save_changes()
        await self._service_uow.close()
