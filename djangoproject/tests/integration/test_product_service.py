import uuid
import pytest
from icecream import ic
from conftest import users_model, groups_model, courses_model, services
from backend.structures import ProductStatus

from products.models import Course as CourseModel
from products.services import CourseService, ProductItemService
from products.repos import ProductItemRepository, CourseRepository
from products.models import ProductItemNotFound, CourseNotFound
from deals.models import Deal as DealModel, DealNotFound

@pytest.mark.product
class TestCourse:
    def test_course_archive_activate_remove(self, courses_model, repos, services):
        course_service: CourseService = services['course_service']
        course1: CourseModel = courses_model['course1']
        # initial validation
        assert isinstance(course1.status, ProductStatus)
        assert course1.status == ProductStatus.ACTIVE

        # ARCHIVATE the course
        course_service.archive(course1.pk) #make status archived & delete all relations in deals
        course1.refresh_from_db()
        assert course1.status == ProductStatus.ARCHIVED

        # delete the course
        # there are no related contracts yet, so cours should be removed properly
        course_service.activate(course1.pk); course_service.remove(course1.id)
        assert not CourseModel.objects.filter(pk=course1.pk).exists() # course must not exist



# @pytest.mark.pi
# class TestProducItem:
#     def test_pi_create(self, courses_model, productitems_model, deals_model, services):
#         pi_service: ProductItemService = services['pi_service']
#         course1: CourseModel = courses_model['course1']
#         deal1: DealModel = deals_model['deal1']

#         #Trying to create new product item bounded to valid deal
#         pi1 = pi_service.create(
#             course_id = course1.pk,
#             deal_id = deal1.pk
#         )
#         assert ProductItemModel.objects.filter(pk=pi1.pk).exists()
#         assert pi1.deal.pk == deal1.pk
#         # ic(pi1.deal.title)
#         # ic(pi1.course.name)

#         with pytest.raises(CourseNotFound):
#             pi2 = pi_service.create(
#                 course_id=uuid.uuid4(), #!
#                 deal_id=deal1.pk
#             )
#         with pytest.raises(DealNotFound):
#             pi2 = pi_service.create(
#                 course_id=course1,
#                 deal_id=uuid.uuid4() #!
#             )