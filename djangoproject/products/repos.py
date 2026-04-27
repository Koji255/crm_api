from uuid import UUID
from typing import List
from backend.interfaces import BaseRepository, AbstractRepository
from django.db.models import QuerySet, Sum, F, Count, Q
from backend.structures import ProductStatus
from .models import Course
from .models import CourseNotFound

class CourseRepository(BaseRepository):
    session = Course

    def list_popular_courses(self, n:int=3) -> List[str]:
        qs = self.session.objects.annotate(
            # get a count from * disticted deals (that are actually won) bounded to some course
            purchases=Count('di_from_course__deal', distinct=True, filter=(Q(di_from_course__deal__contract__isnull=False)))
        ).order_by('-purchases')[:n]
        return qs.values_list('name', flat=True)