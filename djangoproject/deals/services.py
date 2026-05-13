import uuid
from typing import List
from decimal import Decimal
from django.db import transaction
from django.db.utils import IntegrityError
from django.utils import timezone
from django.db.models import QuerySet, F, Sum, DecimalField

from backend.structures import DealStatus
from products.models import Course#, ProductItem
# from accounts.repos import AccountRepository
# from products.services import ProductItemService
from .models import Deal, DealItem, DealNotFound, DealNotAvailable, DealItemNotFound, DealCanNotUpdate
from .repos import DealRepository, DealItemRepository
from contracts.repos import ContractRepository

class DealService():
    def __init__(self, account_service=None, contract_service=None):
        self.deal_repo = DealRepository()
        self.di_repo = DealItemRepository()
        self.contract_repo = ContractRepository()
        self.account_service = account_service
        self.contract_service = contract_service

    def _get_deal(self, id: uuid.UUID) -> Deal:
        '''Returns Course model object. Later replace with dto'''
        try:
            return self.deal_repo.get(id=id)
        except Deal.DoesNotExist as e:
            raise DealNotFound(f'{DealNotFound.MSG}\nDetails:{e}')
        
    def _get_di(self, id: uuid.UUID) -> DealItem:
        '''Returns Deal Item model object. Later replace with dto'''
        try:
            return self.di_repo.get(id=id)
        except DealItem.DoesNotExist as e:
            raise DealItemNotFound(f'{DealItemNotFound.MSG}\nDetails:{e}')

    def _calc_exp_val(self, id: uuid.UUID) -> Decimal:
        '''from DealItem sum of products of 2 columns from join with Course'''
        res = self.deal_repo.session.objects.filter(pk=id).aggregate( # Try to migrate on session.filter
            total = Sum(
                F('di_from_deal__course__unit_price') * F('di_from_deal__quantity') * F('di_from_deal__access_months'), # add discount
                output_field=DecimalField()
            )
        )['total'] or Decimal('0')#!!
        return res
    
    @transaction.atomic()
    def update_exp_val(self, id: uuid.UUID) -> int:
        '''Returns 1 if updated & 0 if no rows affected'''
        return self.deal_repo.update(id=id, expected_value=self._calc_exp_val(id=id))
    
    @transaction.atomic
    def open(self, **kwargs)-> Deal:
        #than, in aggregate update account's status
        # if 'account_id' not in kwargs or not isinstance(kwargs['account_id'], uuid.UUID):
        #     raise DealNotFound(DealNotFound.MSG)
        deal= self.deal_repo.save(**kwargs)
        self.account_service.update_status(id=deal.account.pk)
        return deal

    @transaction.atomic()
    def close(self, id: uuid.UUID, status: DealStatus=DealStatus.WON, loss_reason: str|None=None) -> Deal:
        #Workflow: DealService.close(); ContractService.open() (if deal.is_won); AccountService.update_stats
            n = self.deal_repo.update(id=id, status=status,loss_reason=loss_reason, closed_at=timezone.now())
            if n == 0: raise DealNotFound(f'{DealNotFound.MSG}')

            deal = self._get_deal(id=id)
            if status == DealStatus.WON:
                self.contract_service.open(deal_id=deal.pk)#close deal entity & return affected rows
                # self.deal_repo.update(id=id, contract)
            self.account_service.update_status(id=deal.account_id)
            deal.refresh_from_db() # because of deal.contract_id update in contract service
            return deal

    def add_item(self, deal_id: uuid.UUID, **di_kwargs) -> DealItem:
        with transaction.atomic():
            # Try to merge into 1 qur
            if self.contract_repo.session.objects.filter(deal_from_contract__id=deal_id).exists():
                raise DealCanNotUpdate(DealCanNotUpdate.MSG)
            di = self.di_repo.save(deal_id=deal_id, **di_kwargs)
            updated: int = self.update_exp_val(id=deal_id)
            if not updated: raise DealNotFound(DealNotFound.MSG)
            return di

    def remove_item(self, di_id: uuid.UUID, deal_id: uuid.UUID|None=None)-> None:
        '''
        Removes item from the deal.\n
        *NOT FROM DATABASE*
        '''
        # di = self._get_di(id=di_id)
        # di.deal = None; di.save()
        with transaction.atomic():
            if not deal_id:
                di = self._get_di(id=di_id)
                deal_id = di.deal_id

            self.di_repo.delete(id=di_id) # Delete di
            updated: int = self.update_exp_val(id=deal_id)
            if not updated: raise DealNotFound(DealNotFound.MSG)