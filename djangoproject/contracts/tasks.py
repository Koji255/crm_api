from uuid import UUID
from typing import List
from django.core.mail import send_mail, send_mass_mail
from celery import shared_task
from .services import ContractService

@shared_task
def update_contract_status():
    service = ContractService()
    qs = service.contract_repo.list()
    for q in qs:
        service.update_status(q.pk) # looks weird. Can be better in service & repo

@shared_task
def mail_contract_opened(contract_id: UUID, contact_emails: List[str]):
    send_mass_mail(
        datatuple=(
            (f'Contract {contract_id} opened', 'Some message will be placed here', 'server@gmail.com', contact_emails),
        )
    )