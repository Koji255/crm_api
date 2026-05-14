from uuid import UUID
from typing import List
from django.core.mail import send_mail, send_mass_mail
from celery import shared_task
from .services import ContractService

@shared_task
def update_contract_status():
    '''Beat operation.Operates daily at 00:00 utc+3'''
    service = ContractService()
    qs = service.contract_repo.list()
    for q in qs:
        service.update_status(q.pk)

@shared_task
def mail_contract_opened(contract_id: UUID, contact_emails: List[str]):
    send_mass_mail(
        datatuple=(
            (f'Contract {contract_id} opened', 'Dear client, we opened a contract for you', 'server@gmail.com', contact_emails),
        )
    )