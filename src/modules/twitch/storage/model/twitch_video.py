import twitchio
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src import EVideoType, EDownloadStatus
from src.modules.general.storage.model import Video


class TwitchVideo(Video):
    __tablename__ = "twitch_video"

    id = Column(Integer, ForeignKey("video.id"), primary_key=True)
    external_id = Column(Integer, primary_key=True, autoincrement=False, index=True)
    duration = Column(String(32))
    language = Column(String(32))
    published_at = Column(DateTime(timezone=True))
    thumbnail_url = Column(String(256))
    type = Column(String(32))
    broadcaster_id = Column(Integer, ForeignKey("twitch_broadcaster.external_id"))
    url = Column(String(256))

    broadcaster = relationship("TwitchBroadcaster", back_populates="videos")
    clips = relationship("TwitchClip", back_populates="source_video", primaryjoin="TwitchVideo.external_id == TwitchClip.video_id")

    __mapper_args__ = {
        "polymorphic_identity": EVideoType.TWITCH_VIDEO,
    }

    def __init__(self, video: twitchio.Video, should_download: bool = True):
        self.external_id = video.id
        self.created_at = video.created_at
        self.title = video.title
        self.description = video.description
        self.download_status = EDownloadStatus.PENDING if should_download else EDownloadStatus.DO_NOT_DOWNLOAD
        self.duration = video.duration
        self.language = video.language
        self.published_at = video.published_at
        self.thumbnail_url = video.thumbnail_url
        self.type = video.type
        self.broadcaster_id = video.user.id
        self.url = video.url

    def __repr__(self):
        return f"TwitchVideo ({self.id} | {self.url}) {self.title}"
