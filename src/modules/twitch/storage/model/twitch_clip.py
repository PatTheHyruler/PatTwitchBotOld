from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from twitchio import Clip

from src import EVideoType, EDownloadStatus
from src.modules.general.storage.model import Video


class TwitchClip(Video):
    __tablename__ = "twitch_clip"

    id = Column(Integer, ForeignKey("video.id"), primary_key=True)
    external_id = Column(String(256), primary_key=True)

    broadcaster_id = Column(Integer, ForeignKey("twitch_broadcaster.external_id"))
    creator_id = Column(Integer, ForeignKey("twitch_broadcaster.external_id"))
    video_id = Column(Integer, ForeignKey("twitch_video.external_id"))

    duration = Column(String(32))
    language = Column(String(32))
    thumbnail_url = Column(String(256))
    vod_offset = Column(Integer)

    broadcaster = relationship("TwitchBroadcaster", back_populates="clips", primaryjoin="TwitchClip.broadcaster_id == TwitchBroadcaster.external_id", lazy="joined")
    creator = relationship("TwitchBroadcaster", back_populates="created_clips", primaryjoin="TwitchClip.creator_id == TwitchBroadcaster.external_id", lazy="joined")
    source_video = relationship("TwitchVideo", back_populates="clips", primaryjoin="TwitchClip.video_id == TwitchVideo.external_id", lazy="joined") if video_id is not None else None

    __mapper_args__ = {
        "polymorphic_identity": EVideoType.TWITCH_CLIP
    }

    @property
    def url(self) -> str:
        return f"https://clips.twitch.tv/{self.external_id}"

    @property
    def embed_url(self) -> str:
        return f"https://clips.twitch.tv/embed?clip={self.external_id}"

    def __init__(self, clip: Clip, should_download: bool = True):
        self.created_at = clip.created_at
        self.external_id = clip.id
        self.title = clip.title
        self.download_status = EDownloadStatus.PENDING if should_download else EDownloadStatus.DO_NOT_DOWNLOAD
        self.broadcaster_id = clip.broadcaster.id
        self.creator_id = clip.creator.id
        try:
            self.video_id = int(clip.video_id)
        except ValueError:
            pass
        self.duration = clip.duration
        self.language = clip.language
        self.thumbnail_url = clip.thumbnail_url
        self.vod_offset = clip.vod_offset

    def __repr__(self):
        return f"TwitchClip ({self.id} | {self.url}) {self.title}"
