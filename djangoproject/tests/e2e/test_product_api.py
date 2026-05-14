import pytest
from rest_framework.test import APIClient
from icecream import ic
from typing import Dict, Any

@pytest.mark.e2e
class TestProductApi:
    courses_params = [
        ("CourseA", "Description 1", 1000, "lms-001"),
        ("CourseB", "Description 2", 2500, "lms-002"),
        ("CourseC", "Description 3", 0, "lms-003"),
    ]

    @pytest.mark.parametrize('name, description, unit_price, lms_course_ref', courses_params)
    def test_product_create_get_update_destroy(self, fa_client: APIClient, name, description, unit_price, lms_course_ref):
        #post a course
        response = fa_client.post(
            '/api/v1/courses/',
            format='json',
            data = {
                'name': name,
                'description': description,
                'unit_price': unit_price,
                'lms_course_ref': lms_course_ref
            }
        )
        assert response.status_code == 201
        assert response.data['lms_course_ref'] == lms_course_ref
        
        #get a posted course
        created_course_id = response.data['id']
        response = fa_client.get(
            f'/api/v1/courses/{created_course_id}/',
            format='json',
        )
        assert response.status_code == 200; ic(response.status_code)
        
        #patch the course
        assert response.data['name'] == name
        new_name = 'new_course_name'
        response = fa_client.patch(
            f'/api/v1/courses/{created_course_id}/',
            content_type='application/json',
            data={
                'name': new_name
            }
        )
        assert response.status_code == 200
        assert response.data['name'] == new_name
        ic(response.data['id'])
        
        #delete the course
        response = fa_client.delete(
            f'/api/v1/courses/{created_course_id}/',
        )
        assert response.status_code == 204

    def test_product_retrieve(self, fa_client: APIClient, courses_model: Dict[str, Any]):
        rsp = fa_client.get(
            path='/api/v1/courses/?limit=100&offset=0', # retrieve first 100 products starting from the first
            content_type='application/json', 
        )
        assert rsp.data is not None#; ic(rsp.data)
        assert rsp.data['count'] > 0; ic(rsp.data['count'])
        assert rsp.data['count'] == len(courses_model)