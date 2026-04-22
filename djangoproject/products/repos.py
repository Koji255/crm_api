from uuid import UUID
from backend.interfaces import BaseRepository, AbstractRepository
from django.db.models import QuerySet
from backend.structures import ProductStatus
from .models import Course
from .models import CourseNotFound

class CourseRepository(BaseRepository):
    session = Course