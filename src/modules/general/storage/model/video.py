from sqlalchemy import Column, Integer, String, Enum, DateTime, Text, Boolean
from sqlalchemy.orm import relationship

from src import EVideoType, EDownloadStatus
from .video_author import video_author
from src.database import Base


class Video(Base):
    __tablename__ = "video"

    id = Column(Integer, primary_key=True, autoincrement=True)
    _type = Column(Enum(EVideoType))
    created_at = Column(DateTime(timezone=True))

    title = Column(String(256))
    description = Column(Text)

    filename = Column(String(256))
    directory = Column(String(256))
    download_status = Column(Enum(EDownloadStatus))
    online = Column(Boolean, default=True)

    authors = relationship("Author", secondary=video_author, back_populates="videos", lazy="subquery")

    __mapper_args__ = {
        "polymorphic_identity": EVideoType.VIDEO,
        "polymorphic_on": _type
    }
