from uuid import UUID
from django.db.models import QuerySet
from backend.interfaces import AbstractRepository
from .models import Deal, DealItem

class DealRepository(AbstractRepository):
    def __init__(self):
        self.session = Deal

    def save(self, **kwargs): pass

    def get(self, id): pass

    def list(self): pass

    
class DealItemRepository(AbstractRepository):
    def __init__(self):
        self.session = DealItem

    def save(self, **kwargs) -> DealItem:
        inst, _ = self.session.objects.update_or_create(**kwargs)
        return inst
    
    def get(self, id: UUID) -> DealItem:
        return self.session.objects.get(pk=id)
    
    def list(self) -> QuerySet[DealItem]:
        return self.session.objects.all()