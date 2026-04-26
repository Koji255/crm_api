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
        from .tasks import mail_contract_opened

        #  requires real db like postgres to workk
        with transaction.atomic():
            contract = self.contract_repo.save()
            self.deal_repo.session.objects.filter(pk=deal_id).update(contract_id=contract.pk)
            start_date = timezone.now().date()
            # self.di_repo.session.objects.filter(deal__contract_id=contract.pk).update(
            #     start_date = date,
            #     end_date = ExpressionWrapper(
            #         F('access_months') * timedelta( weeks=4 ) + date, # get access months & convert to weeks per di
            #         output_field=models.DateField()
            #     )
            # )
            qs = self.di_repo.session.objects.select_for_update().filter(deal__contract_id=contract.pk)
            for q in qs: # Potential n+1
                q.start_date = start_date
                q.end_date = start_date + timedelta(weeks=4*q.access_months)
                # q.save()
            qs.bulk_update(qs, fields=['start_date', 'end_date']) # n+1 fix

            contact = contract.deal_from_contract.primary_contact
            if contact:
                mail_contract_opened.delay(contract_id=contract.pk, contact_emails=[contact.email])
            return contract
        
    def update_status(self, id: uuid.UUID) -> None:
        '''If * deal items (bounded to this contract) are outdated, contract becomes expired'''
        active_dis = self.di_repo.list_active_dis_by_contract(contract_id=id, current_date=timezone.datetime.date().today()) #new n+1 prblm
        if not active_dis.exists():
            self.contract_repo.update(id=id, status=ContractStatus.EXPIRED)