from uuid import UUID, uuid4
from typing import TypeVar
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from backend.structures import ACCOUNT_TYPES, ACCOUNT_STATUSES, COUNTRIES
from django.db.models import QuerySet

Lead = TypeVar('Lead') # Will be replaced with real entities
Contract = TypeVar('Contract')

'''
1. Define uneditable fields in update in classes
2. uow via atomic transactions (django builtin)
'''

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
    #FK Contract
    #FK Lead

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
    
    # @staticmethod
    # def update_data(account_id: UUID, **fields) -> None:
    #     #uneditable_fields = set(); fields = set(fields.keys()); if a&b: raise exc
    #     updated: int = Account.objects.filter(pk=account_id).update(**fields)
    #     if not updated:
    #         raise Account.DoesNotExist('Account not found')
        
    def update_status(self) -> None:
        '''function must be manually called after every state transition in leads & contracts (related with linked account)'''
        #New account sets automaticaly
        leads = Lead.objects.filter(account_id=self.pk)
        contracts = Contract.objects.filter(account_id=self.pk)
        new_status = None

        if leads.exists() and self.status != 'LEAD': # Mb prblms (LEAD instead of lead)
            new_status = 'LEAD'; self.update_data(self.id, status=new_status)
        elif contracts.exists() and self.status != 'CUSTOMER': #!
            new_status = 'CUSTOMER'; self.update_data(self.id, status=new_status)
    
    # def list_contacts(self) -> QuerySet:
    #     return Contact.objects.filter(account__id=self.id).only('id', 'first_name', 'last_name', 'email')
    
# class Contact(models.Model): ...
# class AccountContactM2M(models.Model): ...
class Contact(models.Model):
    #No contact entity without an account
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255) #required field
    phone = PhoneNumberField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=True)

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='contacts') #many(contacts)2one(account)

    class Meta:
        unique_together = ['first_name', 'email', 'phone', 'account']

    def __str__(self):
        return f'{self.id}\n{self.email}'

    @staticmethod
    def update_data(contact_id: UUID, **fields) -> None:
        #uneditable_fields = set(); fields = set(fields.keys()); if a&b: raise exc
        updated: int = Contact.objects.filter(pk=contact_id).update(**fields)
        if not updated:
            raise Account.DoesNotExist('Contact not found')