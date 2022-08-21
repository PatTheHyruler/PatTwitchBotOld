import asyncio

from src import Database
from src import TwitchBot
from src.config import Config


async def startup():
    twitch_client_secret = Config.get().Twitch.ClientSecret
    twitch_access_token = Config.get().Twitch.AccessToken
    twitch_command_prefix = Config.get().Twitch.CommandPrefix

    database_host = Config.get().Database.Host
    database_user = Config.get().Database.User
    database_password = Config.get().Database.Password
    database_name = Config.get().Database.Name

    database = Database(
        f"mariadb+asyncmy://{database_user}:{database_password}@{database_host}/{database_name}?charset=utf8mb4"
    )
    bot = TwitchBot(
        token=twitch_access_token,
        prefix=twitch_command_prefix,
        client_secret=twitch_client_secret,
        initial_channels=Config.get().Twitch.InitialChannels,
        database=database
    )

    await database.init()

    print("Loading modules")
    # bot.load_module(name="src.modules.twitch_monitor")
    bot.load_module(name="src.modules.chat_bot")
    # bot.load_module(name="src.modules.test")
    print("Finished loading modules")

    # await database.drop_tables()
    # await database.create_tables()

    await bot.start()


if __name__ == '__main__':
    try:
        asyncio.run(startup())
    except KeyboardInterrupt:
        pass
