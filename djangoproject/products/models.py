from uuid import UUID, uuid4
from decimal import Decimal
from django.db import models
from django.utils.timezone import datetime
from django.db.models import Q
from backend.structures import CurrencyCode, ProductStatus
from django.db.models import QuerySet
from django.db import transaction, IntegrityError
from typing import List, Dict, Optional, Union, TypeVar

from backend.structures import ProductStatus
# from deals.models import Deal
# from contracts.models import Contract

CourseObject = TypeVar('Course')

class CourseNotFound(Exception):
    MSG = 'Object with given id does not exist'
class ProductItemNotFound(Exception):
    MSG = 'Object with given id does not exist'

# Create your models here.
class Course(models.Model):
    #Webhooks as controlers
    #can be deleted if & only if no link relations in leads & contracts. Else just change status
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=ProductStatus.choices, default=ProductStatus.ACTIVE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, choices=CurrencyCode.choices, default=CurrencyCode.USD)
    lms_course_ref = models.CharField(max_length=255, blank=True, null=True) #link to course entity in lms (with content)
    created_at = models.DateTimeField(auto_now_add=True,  editable=False)
    updated_at = models.DateTimeField(auto_now=True,  editable=True)

    class Meta:
        unique_together = ['name', 'lms_course_ref']

    def __str__(self):
        return f'ID: {self.id} | Name: {self.name} | Ref: {self.lms_course_ref}'
    
    @property
    def is_active(self) -> bool:
        return self.status == ProductStatus.ACTIVE
    
    @property
    def is_archived(self) -> bool:
        return self.status == ProductStatus.ARCHIVED

    @property
    def has_relations(self) -> bool:
        '''Returns true if there are already product items bounded to this course instance'''
        return self.pis_from_course.prefetch_related('deal').exists()

    # def list_relations(self) -> QuerySet:
    #     '''Do later'''
    #     deals = ...
    #     contracts = ...
    #     return []

class ProductItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    quantity = models.PositiveIntegerField(default=1)
    access_months = models.PositiveIntegerField(default=1)
    #start_date&end_date will be set after contract creation in service
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    # discount_percent = models.DecimalField(decimal_places=2, default=0)

    course = models.ForeignKey('products.Course', on_delete=models.CASCADE, related_name='pis_from_course')
    deal = models.ForeignKey('deals.Deal', on_delete=models.CASCADE, related_name='pis_from_deal')

    @property
    def total_cost(self) -> Decimal:
        return Decimal(f'{ self.course.unit_price * self.quantity * self.access_months }') # later add discount