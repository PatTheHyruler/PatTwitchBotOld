import logging
from abc import ABCMeta
from typing import TypeVar, Generic, Optional, Dict

from sqlalchemy import select, exists, delete, update

from .base_storage_repository import BaseStorageRepository
from .database import Base
from ..utils import Utils

TEntity = TypeVar("TEntity", bound=Base)
_logger = logging.getLogger(__name__)


class BaseStorageExtendedRepository(BaseStorageRepository[TEntity], Generic[TEntity], metaclass=ABCMeta):
    async def exists_external(self, external_id: str) -> bool:
        stmt = select(self._table).where(self._table.external_id == external_id)
        stmt = exists(stmt).select()
        result = await self._execute_scalars(stmt)
        return result.one()

    async def get_by_external_id(self, external_id: str or int) -> Optional[TEntity]:
        stmt = select(self._table).where(self._table.external_id == external_id)
        return await self._first(stmt)

    async def remove_by_external_id(self, external_id: str or int) -> Optional[TEntity]:
        entity = await self.get_by_external_id(external_id)
        stmt = delete(self._table).where(self._table.external_id == external_id)
        await self._session.execute(stmt)

        _logger.info(entity, "Removed")
        return entity

    async def upsert_external(self, entity: TEntity) -> TEntity:
        if await self.exists_external(entity.external_id):
            return await self.update_entity_external(entity)

        return await self.add(entity)

    async def update_external(self, external_id: int, values: Dict[str, any]) -> TEntity:
        entity: TEntity = await self.get_by_external_id(external_id)

        for table_class, keys in entity.get_constructor_keys().items():
            relevant_values = {}
            for key in keys:
                if key in values:
                    relevant_values[key] = values[key]
            try:
                stmt = update(table_class).where(table_class.external_id == external_id).values(relevant_values)
            except AttributeError:
                stmt = update(table_class).where(table_class.id == entity.id).values(relevant_values)

            await self._session.execute(stmt)

        _logger.info(entity, "Updated")
        return entity

    async def update_entity_external(self, entity: TEntity) -> TEntity:
        return await self.update_external(entity.external_id, Utils.get_class_fields(entity))
