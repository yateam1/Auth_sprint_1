from abc import ABC, abstractmethod
from uuid import UUID

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
        # TODO
        pass

    def update(self, instance, **kwargs):
        # TODO
        pass

    def delete(self, instance):
        db.session.delete(instance)
        db.session.commit()
        return instance
