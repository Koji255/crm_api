import uuid
import pytest
from conftest import users_model, groups_model, courses_model, services
from backend.structures import ProductStatus

from products.models import Course as CourseModel
from products.services import CourseService

@pytest.mark.product
class TestCourse:
    def test_course_crud(self, courses_model, services):
        course_service: CourseService = services['course_service']

        data = {'id': uuid.uuid4(), 'name': 'test_course', 'price': 25.00}
        res = course_service.create(**data) #if course succesfully created, res will get 1
        assert res == True
        #Idempotency check
        res = course_service.create(**data)
        assert res == True

        #Trying to fetch created entity from db
        course = course_service.get(course_id=data['id'])
        assert course.name == data['name']

        #Update some field in instance
        course_service.update(course_id=data['id'], name='test_course1')
        course = course_service.get(course_id=data['id'])
        assert course.name == 'test_course1'
        
        #Update non-existing field on existing course (idempotency)
        with pytest.raises(Exception):
            updated_rows = course_service.update(course_id=data['id'], some_non_existing_row='some_value')
            assert updated_rows == 0

        # Try to update field on non-existing course entity
        with pytest.raises(Exception):
            course_service.update(course_id='non-existing-id', name='test_course1')

        # Delete course
        status = course_service.delete(data['id']) #delete returns status of operation (DELETED or ARCHIVED)
        assert status == ProductStatus.DELETED
        assert course_service.list().filter(pk=data['id']).exists() == False #No such a course in db

        status = course_service.delete(data['id']) # Idempotency check
        assert status == ProductStatus.DELETED