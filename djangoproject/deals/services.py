import uuid
from django.db.models import QuerySet
from django.db import transaction
from django.db.utils import IntegrityError
from products.models import Course
from .models import Deal, DealNotFound


class DealService():
    # def _get_deal(self, deal_id: uuid.UUID) -> Course:
    #     '''Returns Course model object. Later replace with dto'''
    #     try:
    #         deal = Deal.objects.get(pk=deal_id)
    #     except Deal.DoesNotExist as e:
    #         raise DealNotFound(f'{DealNotFound.MSG}\nDetails:{e}')
    #     return deal
   
    # def create(self, **kwargs) -> Course:
    #     '''Later will return dto instead of model'''
    #     try:
    #        course, _ = Course.objects.get_or_create(**kwargs)
    #     except IntegrityError as e:
    #        raise ValueError(f'Cannot create a course with such params\nkwargs{kwargs}\nDetails: \n{e}')
    #     return course
    
    # def get(self, course_id: uuid.UUID) -> Course:
    #     # a bit weird
    #     return self._get_course(course_id)
    
    # def update(self, course_id: uuid.UUID, **kwargs) -> Course:
    #     '''Returns amount of rows affected by an update method'''
    #     with transaction.atomic():
    #         courses = Course.objects.filter(pk=course_id)
    #         if not courses.exists():
    #             raise DealNotFound(f'{DealNotFound.MSG}\nID: {course_id}')
    #         courses.update(**kwargs)
    #         return courses.first()
        
    # def list(self) -> QuerySet:
    #     return Course.objects.all()
    
    # def delete(self, course_id: uuid.UUID) -> ProductStatus: 
    #     '''Course can be removed if & only if it has no relations in deals & contracts.\nElse only status will be changed (on archieved)'''
    #     with transaction.atomic():
    #         #Try for idempotency
    #         try:
    #             course = self._get_course(course_id=course_id) #Race risk
    #             if course.has_relations:
    #                 course.status = ProductStatus.ARCHIVED # make update logic
    #                 course.save(); status = course.status
    #             else:
    #                 course.delete(); status = ProductStatus.DELETED
    #         except DealNotFound:
    #             status = ProductStatus.DELETED
    #         return status


    def make_title(self, deal_id: uuid.UUID, organization: str, owner: str):
        ...
        # hash_ = str(uuid.uuid4())[:4]
        # courses = Course.objects.filter(productitem__deal_id=deal_id).values_list('name', flat=True)
        # res = [hash_, organization, owner] + list(courses)
        # return '_'.join(res)
    def make_expected_value(self, *args): ...
    def close_deal(self, *args): ...