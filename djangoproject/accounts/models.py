from uuid import UUID, uuid4
from typing import TypeVar
from django.db import models
from backend.structures import ACCOUNT_TYPES, ACCOUNT_STATUSES, COUNTRIES

Lead = TypeVar('Lead') # Will be replaced with real entities
Contract = TypeVar('Contract')

# Create your models here.
class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    account_type = models.CharField(choices=ACCOUNT_TYPES, max_length=255, default='OTHER')
    status = models.CharField(choices=ACCOUNT_STATUSES, max_length=255, default='NEW')
    country = models.CharField(choices=COUNTRIES, max_length=255, default='OTHER')
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=True)

    def __str__(self):
        return f'{self.id}: {self.name} | {self.country}'

    def save(self, *args, **kwargs):
        # Check if such an account already in db
        # Replace later with Meta constraints (UniqueConstraint)
        accounts = Account.objects.filter(
            name=self.name, 
            country=self.country,
            city=self.city,
            address=self.address
        )
        if self.pk:
            accounts = accounts.exclude(pk=self.pk)
        if accounts.exists():
            raise ValueError(f'Such an account already exists ({self.name})')
        
        super().save(*args, **kwargs)
    
    @staticmethod
    def update_fields(self, account_id: UUID, **fields):
        if 'status' in fields:
            raise ValueError('Uneditable fields provided')
        
        updated: int = Account.objects.filter(pk=account_id).update(**fields)
        if not updated:
            raise Account.DoesNotExist('Account not found')
        
    def update_status(self):
        '''function must be manually called after every state transition in leads & contracts (related with linked account)'''
        #New account sets automaticaly
        leads = Lead.objects.filter(account_id=self.pk)
        contracts = Contract.objects.filter(account_id=self.pk)

        if leads.exists() and self.status != 'LEAD': # Mb prblms (LEAD instead of lead)
            self.status = 'LEAD'
        elif contracts.exists() and self.status != 'CUSTOMER': #!
            self.status = 'CUSTOMER'
        self.save()

        return self.status
    
class Contact(models.Model): ...
class AccountContactM2M(models.Model): ...