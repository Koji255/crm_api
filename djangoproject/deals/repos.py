from uuid import UUID
from datetime import datetime
from decimal import Decimal
from django.db.models import QuerySet, Sum, F
from backend.interfaces import AbstractRepository, BaseRepository
from backend.structures import DealStatus
from .models import Deal, DealItem

class DealRepository(BaseRepository):
    session = Deal

    def save(self, **kwargs) -> Deal:
        inst = self.session.objects.create(**kwargs)
        return inst
    
    def count_total_deals(self) -> int:
        return self.session.objects.filter(status=DealStatus.WON).count()

    def count_won_deals(self) -> int:
        return self.session.objects.count()
    
    def total_value_deals(self) -> Decimal:
        return self.session.objects.aggregate(
            ttl=Sum(
                F('di_from_deal__course__unit_price') * F('di_from_deal__quantity') *F('di_from_deal__access_months')
            )
        )['ttl'] or Decimal('0')

class DealItemRepository(BaseRepository):
    session = DealItem

    def list_active_dis_by_deal(self, id: UUID, current_date: datetime.date) -> QuerySet[DealItem]:
        return self.session.objects.filter(deal_id=id, end_date__lt=current_date)
    
    def list_active_dis_by_contract(self, id: UUID, current_date: datetime.date) -> QuerySet[DealItem]:
        return self.session.objects.filter(deal__contract_id=id, end_date__lt=current_date)