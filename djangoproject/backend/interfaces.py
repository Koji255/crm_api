import abc
from uuid import UUID
from typing import TypeVar
from django.db.models import QuerySet

Model = TypeVar('Model') #!

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, refference):
        raise NotImplementedError

    @abc.abstractmethod
    def list(self):
        raise NotImplementedError

class BaseRepository(AbstractRepository):
    session = None

    def save(self, **kwargs) -> Model:
        inst = self.session.objects.update_or_create(**kwargs)
        return inst
    
    def update(self, id: UUID, **kwargs) -> int:
        return self.session.objects.filter(pk=id).update(**kwargs)
    
    def get(self, id: UUID) -> Model:
        return self.session.objects.get(pk=id)
    
    def list(self) -> QuerySet[Model]:
        return self.session.objects.all()
    
    def delete(self, id: UUID) -> None:
        self.session.objects.filter(pk=id).delete()