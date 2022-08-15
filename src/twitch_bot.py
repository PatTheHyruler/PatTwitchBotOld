from typing import Union, Callable, Coroutine

from twitchio.ext import commands

from src import Database


class TwitchBot(commands.Bot):
    def __init__(self, token: str, *, prefix: Union[str, list, tuple, set, Callable, Coroutine], database: Database, **kwargs):
        super().__init__(token, prefix=prefix, **kwargs)
        self.database = database

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
