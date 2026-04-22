import abc
from uuid import UUID
from typing import TypeVar

Model = TypeVar('Model')

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, **kwargs) -> Model:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, refference):
        raise NotImplementedError

    @abc.abstractmethod
    def list(self):
        raise NotImplementedError