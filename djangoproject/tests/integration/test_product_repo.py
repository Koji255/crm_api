import uuid
import pytest
from icecream import ic
from conftest import users_model, groups_model, courses_model, services
from backend.structures import ProductStatus

from products.models import Course as CourseModel#, ProductItem as ProductItemModel
from products.services import CourseService#, ProductItemService
from products.repos import CourseRepository
from products.models import CourseNotFound
from deals.models import Deal as DealModel, DealNotFound
from deals.models import DealItemNotFound

@pytest.mark.product
class TestCourse:
    def test_course_save_get_update_delete(self, courses_model, repos):
        course_repo: CourseRepository = repos['course_repo']

        data = {'id': uuid.uuid4(), 'name': 'test_course', 'unit_price': 25.00}
        res = course_repo.save(**data) #if course succesfully created, res will get 1
        assert res.name == data['name']
        #Idempotency check
        res = course_repo.save(**data)
        assert res.name == data['name']

        #Trying to fetch created entity from db
        course = course_repo.get(id=data['id'])
        assert course.name == data['name']

        #Update some field in instance
        course_repo.update(id=data['id'], name='test_course1')
        course = course_repo.get(id=data['id'])
        assert course.name == 'test_course1'
        
        #Update non-existing field on existing course (idempotency)
        with pytest.raises(Exception):
            course_repo.update(id=data['id'], some_non_existing_row='some_value')

        # Try to update field on non-existing course entity
        with pytest.raises(Exception):
            course_repo.update(id='non-existing-id', name='test_course1')

        # Delete course
        status = course_repo.delete(data['id']) #delete returns status of operation (DELETED or ARCHIVED)
        assert status is None
        assert course_repo.list().filter(pk=data['id']).exists() == False #No such a course in db

        status = course_repo.delete(data['id']) # Idempotency check
        assert status is None