from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship

from src import EAuthorType
from src.database import Base
from .video_author import video_author


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128))
    _type = Column(Enum(EAuthorType))

    videos = relationship("Video", secondary=video_author, back_populates="authors", lazy="subquery")

    last_checked = Column(DateTime(timezone=True))

    __mapper_args__ = {
        "polymorphic_identity": EAuthorType,
        "polymorphic_on": _type
    }
