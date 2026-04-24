from uuid import UUID
from django.db.models import QuerySet
from backend.interfaces import AbstractRepository, BaseRepository
from .models import Deal, DealItem

class DealRepository(BaseRepository):
    session = Deal

    def save(self, **kwargs) -> Deal:
        inst = self.session.objects.create(**kwargs)
        return inst

class DealItemRepository(BaseRepository):
    session = DealItem