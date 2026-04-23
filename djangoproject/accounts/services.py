from uuid import UUID
from django.db.models import QuerySet
from backend.structures import ACCOUNT_STATUSES
from .repos import AccountRepository
from deals.repos import DealRepository
from contracts.repos import ContractRepository

class AccountService():
    def __init__(self):
        self.acc_repo = AccountRepository()
        self.deal_repo = DealRepository()
        self.contract_repo = ContractRepository()

    def update_status(self, id: UUID) -> None:
        '''Needs to upgrade'''
        '''function must be manually called after every state transition in leads & contracts (related with linked account)'''
        #New account sets automaticaly
        leads = self.deal_repo.session.objects.filter(account_id=self.pk)
        contracts = self.contract_repo.session.objects.filter(account_id=self.pk)

        if leads.exists() and self.status != 'LEAD': # Mb prblms (LEAD instead of lead)
            new_status = 'LEAD'
            self.acc_repo.update(id=id, status=new_status)

        elif contracts.exists() and self.status != 'CUSTOMER': #!
            new_status = 'CUSTOMER'
            self.acc_repo.update(id=id, status=new_status)
        
    
    def list_contacts(self) -> QuerySet:
        ...
        # return Contact.objects.filter(account__id=self.id).only('id', 'first_name', 'last_name', 'email')