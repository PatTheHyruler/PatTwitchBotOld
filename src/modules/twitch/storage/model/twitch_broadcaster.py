from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from twitchio import User

from src import EAuthorType
from src.modules.general.storage.model import Author


class TwitchBroadcaster(Author):
    """Broadcaster data from Twitch"""

    __tablename__ = "twitch_broadcaster"

    id = Column(Integer, ForeignKey("author.id"), primary_key=True)
    external_id = Column(Integer, primary_key=True, autoincrement=False, index=True)
    login = Column(String(64), primary_key=True)
    profile_image_url = Column(String(256))
    broadcaster_type = Column(String(32))
    description = Column(Text)

    clips = relationship("TwitchClip", back_populates="broadcaster", primaryjoin="TwitchBroadcaster.external_id == TwitchClip.broadcaster_id", lazy="joined")
    created_clips = relationship("TwitchClip", back_populates="creator", primaryjoin="TwitchBroadcaster.external_id == TwitchClip.creator_id", lazy="joined")
    twitch_videos = relationship("TwitchVideo", back_populates="broadcaster", primaryjoin="TwitchBroadcaster.external_id == TwitchVideo.broadcaster_id", lazy="joined")


    __mapper_args__ = {
        "polymorphic_identity": EAuthorType.TWITCH
    }

    def __init__(self, user: User):
        self.external_id = user.id
        self.login = user.name
        self.name = user.display_name
        self.profile_image_url = user.profile_image
        self.broadcaster_type = user.broadcaster_type
        self.description = user.description

    @property
    def display_name(self):
        return self.name

    @display_name.setter
    def display_name(self, name: str):
        self.name = name

    def __repr__(self):
        return f"TwitchBroadcaster ({self.id} | {self.external_id}) {self.login}"
