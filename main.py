import asyncio
import logging.handlers
import sys

from src import TwitchBot, Database, Config, FileFormatter, ConsoleFormatter

_logger = logging.getLogger(__name__)


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

    _logger.info("Loading modules")
    bot.load_module(name="src.modules.twitch")
    bot.load_module(name="src.modules.twitch_monitor")
    bot.load_module(name="src.modules.chat_bot")
    # bot.load_module(name="src.modules.test")
    _logger.info("Finished loading modules")

    # await database.drop_tables()
    # await database.create_tables()

    await bot.start()


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = logging.handlers.RotatingFileHandler(
            filename='pattwitchbot.log',
            encoding='utf-8',
            maxBytes=32 * 1024 * 1024,  # 32 MiB
            backupCount=5,  # Rotate through 5 files
    )
    file_handler.setFormatter(FileFormatter())
    logger.addHandler(file_handler)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(ConsoleFormatter())
    logger.addHandler(stdout_handler)

    try:
        asyncio.run(startup())
    except KeyboardInterrupt:
        pass
