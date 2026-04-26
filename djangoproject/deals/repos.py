from uuid import UUID
from datetime import datetime
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

    def list_active_dis_by_deal(self, id: UUID, current_date: datetime.date) -> QuerySet[DealItem]:
        return self.session.objects.filter(deal_id=id, end_date__lt=current_date)
    
    def list_active_dis_by_contract(self, id: UUID, current_date: datetime.date) -> QuerySet[DealItem]:
        return self.session.objects.filter(deal__contract_id=id, end_date__lt=current_date)