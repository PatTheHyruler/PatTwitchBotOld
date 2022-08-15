from src import TwitchBot


def prepare(bot: TwitchBot):
    bot.load_module(f"{__name__}.clip_mirror")
