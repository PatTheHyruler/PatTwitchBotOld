from typing import Type, Optional

from sqlalchemy import select
from sqlalchemy.sql.expression import func

from src.database import BaseStorageRepository
from ..model.quote import Quote


class QuoteRepository(BaseStorageRepository[Quote]):
    @property
    def _table(self) -> Type[Quote]:
        return Quote

    async def get_random_quote(self) -> Optional[Quote]:
        stmt = select(self._table).order_by(func.random())
        return await self._first(stmt)
