from src import TwitchBot
from .clip_mirror_cog import ClipMirrorCog
from .routines import Routines
from .services import ServiceUnitOfWork
from .storage import StorageUnitOfWork


def prepare(bot: TwitchBot):
    storage_uow = StorageUnitOfWork(bot.database.session)
    service_uow = ServiceUnitOfWork(bot, storage_uow)

    clip_mirror_cog = ClipMirrorCog(bot, service_uow)
    clip_mirror_routines = Routines(clip_mirror_cog)
    clip_mirror_routines.check_for_new_clips.start()

    bot.add_cog(clip_mirror_cog)
