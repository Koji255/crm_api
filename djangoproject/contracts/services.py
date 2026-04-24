import uuid
from datetime import timedelta
from django.db import transaction
from django.db import models
from django.db.models import QuerySet, F, ExpressionWrapper
from django.db import IntegrityError
from django.utils import timezone
from .models import Contract, ContractNotFound
from .repos import ContractRepository
from deals.repos import DealItemRepository, DealRepository
from deals.models import Deal
from backend.structures import ContractStatus

class ContractService:
    def __init__(self):
        self.contract_repo = ContractRepository()
        self.deal_repo = DealRepository()
        self.di_repo = DealItemRepository()

    def _get_contract(self, contract_id: uuid.UUID) -> Contract:
        '''
        Returns Contract model object. Later replace with dto
        '''
        self.contract_repo.session.objects.filter(end_date_lt=timezone.now()).update(status=ContractStatus.EXPIRED) #костыль, later will upgrade on celery check_expired_contracts
        try:
            contract = Contract.objects.get(pk=contract_id)
        except Contract.DoesNotExist as e:
            raise ContractNotFound(f'{ContractNotFound.MSG}\nDetails:{e}')
        return contract
    
    def open(self, deal_id: uuid.UUID) -> Contract:
        '''Implement async task via celery to make contracts expiration'''
        #requires real db like postgres to work
        with transaction.atomic():
            contract = self.contract_repo.save()
            self.deal_repo.session.objects.filter(pk=deal_id).update(contract_id=contract.pk)
            date = timezone.now().date()
            self.di_repo.session.objects.filter(deal__contract_id=contract.pk).update(
                start_date = date,
                end_date = ExpressionWrapper(
                    F('access_months') * timedelta( weeks=4 ) + date, # get access months & convert to weeks per di
                    output_field=models.DateField()
                )
            )
            return contract