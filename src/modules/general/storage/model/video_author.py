from sqlalchemy import Column, Integer, ForeignKey, Table

from src import Base

video_author = Table(
    "video_author",
    Base.metadata,
    Column("video_id", Integer, ForeignKey("video.id")),
    Column("author_id", Integer, ForeignKey("author.id"))
)
