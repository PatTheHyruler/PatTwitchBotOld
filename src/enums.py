from enum import Enum, auto
from typing import Any


class EAutoName(Enum):
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[Any]) -> Any:
        return name


class EVideoType(EAutoName):
    VIDEO = auto()
    TWITCH_CLIP = auto()
    TWITCH_VIDEO = auto()


class EAuthorType(EAutoName):
    NONE = auto()
    TWITCH = auto()


class EDownloadStatus(EAutoName):
    DO_NOT_DOWNLOAD = auto()
    PENDING = auto()
    IN_PROGRESS = auto()
    DONE = auto()
