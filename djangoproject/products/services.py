import uuid
from django.db import transaction, IntegrityError, DataError
from django.db.models import QuerySet
from typing import Dict

from backend.structures import ProductStatus
from .models import Course
from .models import CourseNotFound #Exceptions


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