import uuid
from django.db import transaction, IntegrityError, DataError
from django.db.models import QuerySet, Q
from typing import Dict
from backend.structures import ProductStatus

from deals.models import Deal, DealItem, DealNotAvailable
from deals.repos import DealItemRepository
from .repos import CourseRepository#, ProductItemRepository
from .models import Course#, ProductItem
from .models import CourseNotFound#, ProductItemNotFound #Exceptions


class CourseService():
    def __init__(self):
        self.course_repo = CourseRepository()
        self.di_repo = DealItemRepository()

    def archive(self, id: uuid.UUID):
        with transaction.atomic():
            course = self.course_repo.get(id)
            if course.is_archived: return
            course.status = ProductStatus.ARCHIVED; course.save()
            #delete pi that is bounded only to deal (by def pi can exist only with deal fk and contract is optional) #btw deal linked to contract, not pi
            #so if no contracts made we can safely remove pi from all references 
            self.di_repo.session.objects.filter( Q(course_id=course.pk) & Q(deal__contract__isnull=True) ).delete()

    def activate(self, id: uuid.UUID):
        course = self.course_repo.get(id)
        if not course.is_active:
            course.status = ProductStatus.ACTIVE; course.save()

    def remove(self, id: uuid.UUID):
        with transaction.atomic():
            # There are already archive() method, that allows to softly change course's status on archived & pop it from * deals, only contracts will store with row
            # So first check contracts existence. If contracts in game, we should make soft status migration using archive
            # else it is possible to forcifully delete the course via repo
            related_contracts: bool = self.di_repo.session.objects.filter( Q(course_id=id) & Q(deal__contract__isnull=False) ).exists()
            if related_contracts:
                self.archive(id); return
            self.course_repo.delete(id)


# class ProductItemService:
#     def _get_pi(self, pi_id: uuid.UUID) -> ProductItem:
#         '''Returns Course model object. Later replace with dto'''
#         try:
#             pi = ProductItem.objects.get(pk=pi_id)
#         except ProductItem.DoesNotExist as e:
#             raise ProductItemNotFound(f'{ProductItemNotFound.MSG}\nDetails:{e}')
#         return pi
    
#     def get(self, pi_id: uuid.UUID) -> ProductItem:
#         # a bit weird
#         return self._get_pi(pi_id)
    
#     def list(self) -> QuerySet:
#         return ProductItem.objects.all()

#     def create(self, **kwargs) -> ProductItem:      
#         '''Later will return dto instead of model'''
#         from deals.services import DealService # Avoiding circular import
#         from products.services import CourseService
        
#         with transaction.atomic():
#             try:
#                 DealService().validate_deal(kwargs.get('deal_id')) #Check deal exists & is deal open or not
#                 CourseService().get(kwargs.get('course_id')) #Checks course existence
#                 pi = ProductItem.objects.create(**kwargs)
#                 return pi
#                 # deal = Deal.objects.get(pk=kwargs.get('deal_id'))
#                 # if not deal.is_open:
#                 #     raise DealNotAvailable(f'{DealNotAvailable.MSG}')
#                 # pi= ProductItem.objects.create(**kwargs)
#                 # return pi

#             except IntegrityError as e:
#                 raise ValueError(f'Cannot create a course with such params\nkwargs{kwargs}\nDetails: \n{e}')
            
#     def update(self, pi_id: uuid.UUID, **kwargs) -> ProductItem:
#         '''Returns updated version of the product item'''
#         with transaction.atomic():
#             pi = self._get_pi(pi_id)
#             for field, val in kwargs.items(): #New ver. of update
#                 setattr(pi, field, val)
#             pi.save()
#             return pi.refresh_from_db()
    
#     def delete(self, pi_id: uuid.UUID) -> None:
#         # self._get_pi(pi_id).delete()
#         ProductItem.objects.filter(pi_id).delete()