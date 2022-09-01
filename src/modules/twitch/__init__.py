from src import TwitchBot
from .services import ServiceUnitOfWork
from .storage import StorageUnitOfWork
from .twitch_api import TwitchAPI


def prepare(bot: TwitchBot):
    storage_uow = StorageUnitOfWork(bot.database.session)
    service_uow = ServiceUnitOfWork(bot, storage_uow)

    twitch_api = TwitchAPI(bot, service_uow)

    bot.add_cog(twitch_api)
