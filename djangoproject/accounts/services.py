import uuid
from django.db.models import QuerySet
from backend.structures import AccountStatus, DealStatus, ContractStatus
from .repos import AccountRepository
from deals.repos import DealRepository
from contracts.repos import ContractRepository
from .models import Account, AccountNotFound

class AccountService():
    def __init__(self):
        self.acc_repo = AccountRepository()
        self.deal_repo = DealRepository()
        self.contract_repo = ContractRepository()

    def _get_account(self, id: uuid.UUID) -> Account:
        '''Returns Deal Item model object. Later replace with dto'''
        try:
            return self.acc_repo.get(id=id)
        except Account.DoesNotExist as e:
            raise AccountNotFound(f'{AccountNotFound.MSG}\nDetails:{e}')

    def update_status(self, id: uuid.UUID) -> None:
        '''Needs to upgrade'''
        '''function must be manually called after every state transition in leads & contracts (related with linked account)'''
        #New account sets automaticaly
        has_contracts = self.contract_repo.session.objects.filter(deal_from_contract__account_id=id).exists()
        has_active_deals = self.deal_repo.session.objects.filter(account_id=id, status=DealStatus.OPEN).exists()

        if has_contracts: 
            self.acc_repo.update(id=id, status=AccountStatus.CUSTOMER)#!
        elif has_active_deals: 
            self.acc_repo.update(id=id, status=AccountStatus.LEAD) # Mb prblms (LEAD instead of lead)
        else:
            self.acc_repo.update(id=id, status=AccountStatus.ACTIVE)
        
    
    def list_contacts(self) -> QuerySet:
        ...
        # return Contact.objects.filter(account__id=self.id).only('id', 'first_name', 'last_name', 'email')