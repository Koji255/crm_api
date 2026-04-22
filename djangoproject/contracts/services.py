import uuid
from django.db.models import QuerySet
from django.db import IntegrityError
from .models import Contract, ContractNotFound
from deals.models import Deal

class ContractService:
    def _get_contract(self, contract_id: uuid.UUID) -> Contract:
        '''
        Returns Contract model object. Later replace with dto
        '''
        try:
            contract = Contract.objects.get(pk=contract_id)
        except Contract.DoesNotExist as e:
            raise ContractNotFound(f'{ContractNotFound.MSG}\nDetails:{e}')
        return contract
    
    # def list(self) -> QuerySet:
    #     return Deal.objects.all().prefetch_related('included_productitems__course')

    # def create(self, **kwargs) -> Deal:
    #     '''Later will return dto instead of model'''
    #     try:
    #         deal = Deal(**kwargs)
    #         if not deal.title:
    #             deal.title = self._make_title(deal_id=deal.pk, account_name=deal.account.name, owner_username=deal.owner.username)
    #         deal.save()
    #     except IntegrityError as e:
    #        raise ValueError(f'Cannot create a deal with such params\nkwargs{kwargs}\nDetails: \n{e}')
    #     return deal

    # def get(self, contract_id: uuid.UUID) -> Contract:
    #     return self._get_deal(contract_id)
    

    
    def create(self, deal_id: uuid.UUID) -> Contract:
        ...