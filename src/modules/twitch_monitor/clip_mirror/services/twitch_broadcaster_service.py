from typing import List

from twitchio import HTTPException, User

from src import BaseService, TwitchBot, BroadcasterNotFound
from ..storage import StorageUnitOfWork
from ..storage.model.twitch_broadcaster import TwitchBroadcaster
from ..storage.repository.twitch_broadcaster_repository import TwitchBroadcasterRepository


class TwitchBroadcasterService(BaseService[TwitchBroadcaster, TwitchBroadcasterRepository, StorageUnitOfWork]):
    def __init__(
            self,
            bot: TwitchBot,
            repository: TwitchBroadcasterRepository,
            storage_uow: StorageUnitOfWork,
    ):
        super().__init__(bot, repository, storage_uow)

    async def fetch_user(self, login: str = None, user_id: int = None) -> User:
        fetch_kwargs = {}
        error_kwargs = {}
        if login is not None:
            fetch_kwargs["names"] = [login]
            error_kwargs["login"] = login
        elif user_id is not None:
            fetch_kwargs["ids"] = [user_id]
            error_kwargs["user_id"] = user_id
        else:
            raise BroadcasterNotFound()

        try:
            users: List[User] = await self.bot.fetch_users(**fetch_kwargs)
        except HTTPException:
            users = []

        if len(users) == 0:
            raise BroadcasterNotFound(**error_kwargs)

        return users[0]

    async def add_twitch_broadcaster(self, login: str) -> TwitchBroadcaster:
        user = await self.fetch_user(login=login)
        return await self.storage_uow.twitch_broadcasters.upsert(TwitchBroadcaster(user))
