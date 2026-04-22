from uuid import UUID
from backend.interfaces import AbstractRepository
from django.db.models import QuerySet
from backend.structures import ProductStatus
from .models import Course, ProductItem
from .models import CourseNotFound, ProductItemNotFound

class CourseRepository(AbstractRepository):
    def __init__(self):
        self.session = Course

    def save(self, **kwargs) -> Course:
        inst, _ = self.session.objects.update_or_create(**kwargs)
        return inst
    
    def update(self, id: UUID, **kwargs) -> Course:
        inst = self.session.objects.filter(pk=id).update(**kwargs)
        return inst
    
    def get(self, id: UUID) -> Course:
        return self.session.objects.get(pk=id)
    
    def list(self) -> QuerySet[Course]:
        return self.session.objects.all()
    
    def delete(self, id: UUID) -> None:
        self.session.objects.filter(pk=id).delete()


class ProductItemRepository(AbstractRepository):
    def __init__(self):
        self.session = ProductItem

    def save(self, **kwargs) -> ProductItem:
        inst, _ = self.session.objects.update_or_create(**kwargs)
        return inst
    
    def get(self, id: UUID) -> ProductItem:
        return self.session.objects.get(pk=id)
    
    def list(self) -> QuerySet[ProductItem]:
        return self.session.objects.all()