from uuid import UUID, uuid4
from django.db import models
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
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True,  editable=True)

    class Meta:
        unique_together = ['name', 'lms_course_ref']

    def __str__(self):
        return f'ID: {self.id} | Name: {self.name} | Ref: {self.lms_course_ref}'
    
    @property
    def has_relations(self) -> bool:
        relations = self.list_relations()
        return True if relations else False #False if len(relations) == 0

    def list_relations(self): #-> List[QuerySet]
        '''Do later'''
        deals = ...
        contracts = ...
        return []

    @classmethod
    def add(cls, **kwargs):
        pass
        # try:
        #    Course.objects.create(**kwargs)
        # except IntegrityError as e:
        #    raise ValueError(f'Cannot create a course with such params\nkwargs{kwargs}\nDetails: \n{e}')
    
    @classmethod
    def get(cls, course_id: UUID): #Make data mapper later (dto)
        pass
        # '''Returns Course model object. Later replace with dto'''
        # try:
        #     course = Course.objects.get(pk=course_id)
        # except cls.DoesNotExist as e:
        #     raise CourseNotFound(f'{CourseNotFound.MSG}\nDetails:{e}')
        # return course

    @classmethod
    def list(cls):
        pass
        # return Course.objects.all()
    
    @classmethod
    def remove(cls, course_id: UUID) -> ProductStatus: 
        pass
        # '''Course can be removed if & only if it has no relations in deals & contracts.\nElse only status will be changed (on archieved)'''
        # with transaction.atomic():
        #     try:
        #         course = cls.objects.get(pk=course_id) #Race risk
        #     except cls.DoesNotExist as e:
        #         raise CourseNotFound(f'{CourseNotFound.MSG}\nDetails:{e}')
        #     if course.has_relations:
        #         course.status = ProductStatus.ARCHIVED # make update logic
        #         course.save(); status = course.status
        #     else:
        #         course.delete(); status = ProductStatus.DELETED
        #     return status
    

class ProductItem(models.Model):
    #Fixed start & end date for all product items in single contract. It will appear in contract entity since creation
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    quantity = models.PositiveIntegerField(default=1)
    # unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    # discount_percent = models.DecimalField(decimal_places=2, default=0)

    course = models.ForeignKey('products.Course', on_delete=models.CASCADE, related_name='created_productitems')
    deal = models.ForeignKey('deals.Deal', on_delete=models.CASCADE, blank=False, null=False, related_name='included_productitems')
    #Contract can be empty cuz deal come up before the contract
    contract = models.ForeignKey('contracts.Contract', on_delete=models.CASCADE, blank=True, null=True, related_name='fixed_productitems')

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    (Q(deal__isnull=False)&Q(contract__isnull=True)) | (Q(deal__isnull=False)&Q(contract__isnull=False)) 
                ),
                name="productitem_belongs_to_deal_or_contract"
            )
        ]

    # def total_price(self) -> str:
    #     return str(self.quantity * self.course.unit_price)