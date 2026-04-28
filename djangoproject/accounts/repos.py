from uuid import UUID
from decimal import Decimal
from django.db.models import QuerySet, Q
from backend.interfaces import AbstractRepository, BaseRepository
from .models import Account

class AccountRepository(BaseRepository):
    session = Account

    def count_all_accounts(self) -> int:
        return self.session.objects.count()
    
    def count_lead_accounts(self) -> Decimal:
        '''Returns the amount of all potential (lead) accounts, except from those, that have contracts'''
        # return self.session.objects.filter(Q(deals_from_account__contract__isnull=True)).distinct().count()
        ...
    
    def count_customer_accounts(self) -> Decimal:
        return self.session.objects.filter(deals_from_account__contract__isnull=False).distinct().count()