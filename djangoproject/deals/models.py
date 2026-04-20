from uuid import uuid4
from django.db import models
from django.contrib.auth import get_user_model
from backend.structures import DealStatus
from django.utils import timezone
from datetime import timedelta
# from products.models import Course

UserModel = get_user_model()

class DealNotFound(Exception):
    MSG = 'Object with given id does not exist'

def default_working_date():
    return timezone.now() + timedelta(weeks=2.0)

class Deal(models.Model):
    #default close_data
    #default title gen
    #expected_value calc
    #close deal. If won, create contract
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True, null=True) # make auto gen
    status = models.CharField(max_length=32, choices=DealStatus.choices, default=DealStatus.OPEN)
    expected_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True, null=True) #Cost (total from all product_items bounded to the deal)
    expected_close_date = models.DateField(null=True, blank=True, default=default_working_date) #!!!
    description = models.TextField(blank=True, null=True)
    loss_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    account = models.ForeignKey('accounts.Account',on_delete=models.CASCADE, related_name='associated_deals')
    owner = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, related_name='managed_deals') # Staff that manages the deal
    primary_contact = models.ForeignKey('accounts.Contact', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_deals') # Main contact face

    class Meta:
        # unique_together = ['title', 'account', 'owner']
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
    
    # def make_title(self):
    #     hash_ = str(uuid4())[:4]
    #     organization = self.account.name
    #     working_manager = self.owner.name
    #     courses = Course.objects.filter(productitem__deal_id=self.pk).values_list('name', flat=True)
    #     res = [hash_, organization, working_manager] + list(courses)
    #     return '_'.join(res)
    
    # def save(self, *args, **kwargs):
    #     if not self.title: #Title auto set
    #         self.title = self.make_title()
    #     return super().save(*args, **kwargs)