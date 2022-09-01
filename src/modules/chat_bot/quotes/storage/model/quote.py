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

    context = Column(String(128))
    local_id = Column(Integer)

    def __init__(self, text: str, added_by: str, added_at: datetime.datetime,
                 context: str = None, local_id: int = None):
        self.quote_text = text
        self.added_by = added_by
        self.added_at = added_at
        self.context = context
        self.local_id = local_id

    @property
    def visible_id(self) -> int:
        return self.local_id if self.local_id is not None else self.id

    def __repr__(self):
        return f"Quote from {self.context} #{self.local_id} ({self.id}): {self.quote_text}"

    def __str__(self):
        return f"Quote #{self.visible_id}: {self.quote_text}"
