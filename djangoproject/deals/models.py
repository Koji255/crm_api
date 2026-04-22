from uuid import uuid4
from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model
from backend.structures import DealStatus
from django.utils import timezone
from datetime import timedelta
# from products.models import Course

UserModel = get_user_model()

class DealNotFound(Exception):
    MSG = 'Object with given id does not exist'
class DealNotAvailable(Exception):
    MSG = 'Given deal is already closed and not available for usage'
class DealItemNotFound(Exception):
    MSG = 'Object with given id does not exist'


def default_working_date():
    return timezone.now() + timedelta(weeks=2.0)

class Deal(models.Model):
    #default close_data
    #default title gen
    #expected_value calc
    #close deal. If won, create contract
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    # title = models.CharField(max_length=255, blank=True, null=True) # make auto gen
    status = models.CharField(max_length=32, choices=DealStatus.choices, default=DealStatus.OPEN)
    expected_value = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0'), blank=True) #Cost (total from all product_items bounded to the deal)
    expected_close_date = models.DateField(null=True, blank=True, default=default_working_date) #!!!
    description = models.TextField(blank=True, null=True)
    loss_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    account = models.ForeignKey('accounts.Account',on_delete=models.CASCADE, related_name='deals_from_account')
    owner = models.ForeignKey(UserModel, on_delete=models.SET_NULL, blank=True, null=True, related_name='deals_from_owner') # Staff that manages the deal
    contract = models.OneToOneField('contracts.Contract', on_delete=models.PROTECT, blank=True, null=True, related_name='deal_from_contract')
    primary_contact = models.ForeignKey('accounts.Contact', on_delete=models.SET_NULL, null=True, blank=True, related_name='deal_from_contact') # Main contact face

    class Meta:
        # unique_together = ['title', 'account', 'owner']
        ordering = ["-created_at"]

    def __str__(self):
        return f'id:{str(self.pk)[:8]}', f'account:{self.account.name}', f'owner:{self.owner.username}'
    
    @property
    def is_open(self) -> bool:
        '''Returns true if deal is open & it is possible to add product items (PIs) in'''
        return self.status == DealStatus.OPEN
    

class DealItem(models.Model):
    '''Also called di'''
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    quantity = models.PositiveIntegerField(default=1)
    access_months = models.PositiveIntegerField(default=1)
    #start_date&end_date will be set after contract creation in service
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    # discount_percent = models.DecimalField(decimal_places=2, default=0)

    course = models.ForeignKey('products.Course', on_delete=models.CASCADE, related_name='di_from_course')
    deal = models.ForeignKey('deals.Deal', on_delete=models.CASCADE, related_name='di_from_deal')

    def __str__(self):
        return f'{str(self.id)[:8]}::course:{self.course.name}::deal:{self.deal.title}'

    @property
    def total_cost(self) -> Decimal:
        return Decimal(f'{ self.course.unit_price * self.quantity * self.access_months }') # later add discount