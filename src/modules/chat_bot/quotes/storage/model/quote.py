import datetime

from sqlalchemy import Column, String, Integer, Text, DateTime

from src.database import Base


class Quote(Base):
    """Broadcaster data from Twitch"""

    __tablename__ = "quote"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quote_text = Column(Text)
    added_by = Column(String(128))
    added_at = Column(DateTime(timezone=True))

    def __init__(self, text: str, added_by: str, added_at: datetime.datetime):
        self.quote_text = text
        self.added_by = added_by
        self.added_at = added_at

    def __str__(self):
        return f"Quote #{self.id}: {self.quote_text}"
