from src import TwitchBot
from .quote_cog import QuoteCog
from .services import ServiceUnitOfWork
from .storage import StorageUnitOfWork


def prepare(bot: TwitchBot):
    storage_uow = StorageUnitOfWork(bot.database.session)
    service_uow = ServiceUnitOfWork(bot, storage_uow)

    quote_cog = QuoteCog(bot, service_uow)

    bot.add_cog(quote_cog)
