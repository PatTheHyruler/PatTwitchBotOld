class ConfigException(Exception):
    def __init__(self, option: str):
        self.option = option


class MissingConfigOption(ConfigException):
    def __str__(self):
        return f"Option {self.option} not found in config!"


class WhitespaceConfigOption(ConfigException):
    def __str__(self):
        return f"Config option {self.option} contains only whitespace!"


class BroadcasterNotFound(Exception):
    def __init__(self, login: str = None, user_id: int = None):
        self.twitch_login = login
        self.twitch_user_id = user_id

    def __str__(self):
        msg = f"Couldn't find Twitch Broadcaster"

        if self.twitch_login is not None:
            return f"{msg} {self.twitch_login}"

        if self.twitch_user_id is not None:
            return f"{msg} {self.twitch_user_id}"

        return f"{msg} (no more info provided)"
