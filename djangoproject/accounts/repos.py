from uuid import UUID
from django.db.models import QuerySet
from backend.interfaces import AbstractRepository, BaseRepository
from .models import Account

class AccountRepository(BaseRepository):
    session = Account

    def count_total_accounts(self) -> int:
        return self.session.objects.count()
    
    def count_customer_accounts(self) -> int:
        return self.session.objects.filter(deals_from_account__contract_id__isnull=False).values('account_id').distinct().count()