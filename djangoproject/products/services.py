import uuid
from django.db import transaction, IntegrityError, DataError
from django.db.models import QuerySet
from typing import Dict

from backend.structures import ProductStatus
from .models import Course, ProductItem
from .models import CourseNotFound, ProductItemNotFound #Exceptions
from deals.models import Deal, DealNotAvailable


class CourseService():
    def _get_course(self, course_id: uuid.UUID) -> Course:
        '''Returns Course model object. Later replace with dto'''
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist as e:
            raise CourseNotFound(f'{CourseNotFound.MSG}\nDetails:{e}')
        return course
   
    def create(self, **kwargs) -> Course:
        '''Later will return dto instead of model'''
        try:
           course, _ = Course.objects.get_or_create(**kwargs)
        except IntegrityError as e:
           raise ValueError(f'Cannot create a course with such params\nkwargs{kwargs}\nDetails: \n{e}')
        return course
    
    def get(self, course_id: uuid.UUID) -> Course:
        # a bit weird
        return self._get_course(course_id)
    
    def update(self, course_id: uuid.UUID, **kwargs) -> Course:
        '''Returns amount of rows affected by an update method'''
        with transaction.atomic():
            courses = Course.objects.filter(pk=course_id)
            if not courses.exists():
                raise CourseNotFound(f'{CourseNotFound.MSG}\nID: {course_id}')
            courses.update(**kwargs)
            return courses.first()
        
    def list(self) -> QuerySet:
        return Course.objects.all()
    
    def delete(self, course_id: uuid.UUID) -> ProductStatus: 
        '''Course can be removed if & only if it has no relations in deals & contracts.\nElse only status will be changed (on archieved)'''
        with transaction.atomic():
            #Try for idempotency
            try:
                course = self._get_course(course_id=course_id) #Race risk
                if course.has_relations:
                    course.status = ProductStatus.ARCHIVED # make update logic
                    course.save(); status = course.status
                else:
                    course.delete(); status = ProductStatus.DELETED
            except CourseNotFound:
                status = ProductStatus.DELETED
            return status
        

class ProductItemService:
    def _get_pi(self, pi_id: uuid.UUID) -> ProductItem:
        '''Returns Course model object. Later replace with dto'''
        try:
            pi = ProductItem.objects.get(pk=pi_id)
        except ProductItem.DoesNotExist as e:
            raise ProductItemNotFound(f'{ProductItemNotFound.MSG}\nDetails:{e}')
        return pi
    
    def get(self, pi_id: uuid.UUID) -> ProductItem:
        # a bit weird
        return self._get_pi(pi_id)
    
    def list(self) -> QuerySet:
        return ProductItem.objects.all()

    def create(self, **kwargs) -> ProductItem:      
        '''Later will return dto instead of model'''
        from deals.services import DealService # Avoiding circular import
        from products.services import CourseService
        
        with transaction.atomic():
            try:
                DealService().validate_deal(kwargs.get('deal_id')) #Check deal exists & is deal open or not
                CourseService().get(kwargs.get('course_id')) #Checks course existence
                pi = ProductItem.objects.create(**kwargs)
                return pi
                # deal = Deal.objects.get(pk=kwargs.get('deal_id'))
                # if not deal.is_open:
                #     raise DealNotAvailable(f'{DealNotAvailable.MSG}')
                # pi= ProductItem.objects.create(**kwargs)
                # return pi

            except IntegrityError as e:
                raise ValueError(f'Cannot create a course with such params\nkwargs{kwargs}\nDetails: \n{e}')
            
    def update(self, pi_id: uuid.UUID, **kwargs) -> ProductItem:
        '''Returns updated version of the product item'''
        with transaction.atomic():
            pi = self._get_pi(pi_id)
            for field, val in kwargs.items(): #New ver. of update
                setattr(pi, field, val)
            pi.save()
            return pi.refresh_from_db()
    
    def delete(self, pi_id: uuid.UUID) -> None:
        # self._get_pi(pi_id).delete()
        ProductItem.objects.filter(pi_id).delete()