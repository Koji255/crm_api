from uuid import UUID
from django.db.models import QuerySet
from backend.interfaces import AbstractRepository, BaseRepository
from .models import Contract

class ContractRepository(BaseRepository):
    session = Contract

    def save(self, **kwargs) -> Contract:
        inst = self.session.objects.create(**kwargs)
        return inst
    
    def update(self, **kwargs) -> None:
        '''Can not update contract entity'''
        return