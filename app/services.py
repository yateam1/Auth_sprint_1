from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional, Iterable

from sqlalchemy import inspect

from app import create_app, db


class AbstractService(ABC):

    @property
    @abstractmethod
    def model(self) -> db.Model:
        pass

    def get_all(self):
        return self.model.query.all(app=create_app())

    def get_by_pk(self, pk: UUID):
        return self.model.query.filter_by(id=pk).first()

    def create(self, **kwargs):
        data = self._filter_kwargs(data=kwargs, exclude=['id', 'created_at', 'updated_at'])
        instance = self.model(**data)
        db.session.add(instance)
        db.session.commit()
        return instance

    def update(self, instance, **kwargs):
        data = self._filter_kwargs(data=kwargs, exclude=['id', 'created_at', 'updated_at'])
        for k, v in data.items():
            setattr(instance, k, v)
        db.session.commit()
        return instance

    def delete(self, instance):
        db.session.delete(instance)
        db.session.commit()
        return instance

    def _fields_name(self) -> set:
        """Возвращает список полей модели."""
        mapper = inspect(self.model)
        return {column.key for column in mapper.attrs}

    def _filter_kwargs(self, data: dict, exclude: Optional[Iterable] = None,):
        """Оставляет только те ключи, которые есть в полях модели."""
        fields = self._fields_name()
        if exclude:
            fields -= set(exclude)
        return {k: v for k, v in data.items() if k in fields}
