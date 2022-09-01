from typing import Type, Optional, List

from sqlalchemy import select, delete
from sqlalchemy.sql.expression import func

from src.database import BaseStorageRepository
from ..model.quote import Quote


class QuoteRepository(BaseStorageRepository[Quote]):
    @property
    def _table(self) -> Type[Quote]:
        return Quote

    async def add(self, entity: Quote) -> Quote:
        if entity.context:
            entity.local_id = await self.get_next_local_id(entity.context)
        return await super().add(entity)

    async def get_all(self, context: str = None) -> List[Quote]:
        stmt = select(self._table)
        if context:
            stmt = stmt.where(self._table.context == context)
        return await self._all(stmt)

    async def get_next_local_id(self, context: str) -> int:
        existing_quotes = await self.get_all(context)
        return max([quote.local_id for quote in existing_quotes if quote.local_id is not None] + [0]) + 1

    async def get_by_local_id(self, context: str, local_id: int) -> Optional[Quote]:
        stmt = select(self._table).where(self._table.context == context).where(self._table.local_id == local_id)
        return await self._first(stmt)

    async def remove_by_local_id(self, context: str, local_id: int) -> Optional[Quote]:
        entity = await self.get_by_local_id(context, local_id)
        if entity is None:
            return
        return await self.remove(entity)

    async def get_random_quote(self, context: str = None) -> Optional[Quote]:
        stmt = select(self._table)
        if context:
            stmt = stmt.where(self._table.context == context)
        stmt = stmt.order_by(func.random())
        return await self._first(stmt)
