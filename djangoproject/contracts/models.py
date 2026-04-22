from uuid import uuid4
from django.db import models

from backend.structures import ContractStatus

class ContractNotFound(Exception):
    MSG = 'Object with given id does not exist'

# Create your models here.
class Contract(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    status = models.CharField(choices=ContractStatus, default=ContractStatus.ACTIVE)
    start_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=True)

    # deal = models.OneToOneField('deals.Deal', on_delete=models.PROTECT, related_name='resulting_contract')