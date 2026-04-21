import uuid
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
    
    def create(self, deal_id: uuid.UUID) -> Contract:
        ...