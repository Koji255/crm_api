from uuid import UUID
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.db.models import QuerySet, F,  Sum
from backend.interfaces import AbstractRepository, BaseRepository
from .models import Contract

class ContractRepository(BaseRepository):
    session = Contract

    def save(self, **kwargs) -> Contract:
        inst = self.session.objects.create(**kwargs)
        return inst
    
    # def update(self, **kwargs) -> None:
    #     '''Can not update contract entity'''
    #     return

    def total_value_contracts(self) -> Decimal:
        return self.session.objects.aggregate(
            ttl=Sum(
                F('deal_from_contract__di_from_deal__course__unit_price') 
                *
                F('deal_from_contract__di_from_deal__quantity') 
                *
                F('deal_from_contract__di_from_deal__access_months')
            )
        )['ttl'] or Decimal('0')
    
    def total_value_last_month_contracts(self) -> Decimal:
        month_ago = timezone.now()-timedelta(days=30)
        #filter by contracts that were created in last moth
        return self.session.objects.filter(created_at__gte=month_ago).aggregate(
            ttl=Sum(
                F('deal_from_contract__di_from_deal__course__unit_price') 
                *
                F('deal_from_contract__di_from_deal__quantity') 
                *
                F('deal_from_contract__di_from_deal__access_months')
            )
        )['ttl'] or Decimal('0')