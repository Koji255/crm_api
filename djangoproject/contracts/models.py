from uuid import uuid4
from django.db import models

from backend.structures import ContractStatus

class ContractNotFound(Exception):
    MSG = 'Object with given id does not exist'

# Create your models here.
class Contract(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    status = models.CharField(choices=ContractStatus, default=ContractStatus.ACTIVE)
    # start_date = models.DateTimeField(auto_now_add=True)
    # end_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, editable=False)
    updated_at = models.DateField(auto_now=True, editable=True)

    # deal = models.OneToOneField('deals.Deal', on_delete=models.PROTECT, related_name='contract_from_deal')

    def __str__(self):
        return f'{str(self.id)[:8]}::status:{self.status}'
    
    @property
    def is_active(self):
        return self.status == ContractStatus.ACTIVE