import uuid
import pytest
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

    def archive(self, id: uuid.UUID) -> Course:
        with transaction.atomic():
            course = self.course_repo.get(id)
            if course.is_archived: return
            course.status = ProductStatus.ARCHIVED; course.save()
            #delete pi that is bounded only to deal (by def pi can exist only with deal fk and contract is optional) #btw deal linked to contract, not pi
            #so if no contracts made we can safely remove pi from all references 
            self.di_repo.session.objects.filter( Q(course_id=course.pk) & Q(deal__contract__isnull=True) ).delete()
            return course

    def activate(self, id: uuid.UUID) ->Course:
        course = self.course_repo.get(id)
        if not course.is_active:
            course.status = ProductStatus.ACTIVE; course.save()
        return course

    def remove(self, id: uuid.UUID):
        with transaction.atomic():
            # There are already archive() method, that allows to softly change course's status on archived & pop it from * deals, only contracts will store with row
            # So first check contracts existence. If contracts in game, we should make soft status migration using archive
            # else it is possible to forcifully delete the course via repo
            related_contracts: bool = self.di_repo.session.objects.filter( Q(course_id=id) & Q(deal__contract__isnull=False) ).exists()
            if related_contracts:
                self.archive(id); return
            self.course_repo.delete(id)