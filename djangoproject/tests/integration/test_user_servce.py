import pytest
from conftest import users_model, groups_model, services
from django.contrib.auth.models import Group
from users.models import User
from users.services import UserService
from djangoproject.backend.structures import GroupEnum

@pytest.mark.user
class TestUser:
    def test_role_set_revoke(self, users_model, groups_model, services):
        user: User = users_model['manager1']
        group: Group = groups_model
        user_service: UserService = services['user_service']
        
        #Check that entity has a group from initialization in conftest
        assert user.groups.first().name == GroupEnum.MANAGER.value
        #Revoke role from user
        user_service.revoke_role(user_id=user.pk)
        assert user.groups.filter().exists() == False
        
        # Idempotency check
        user_service.revoke_role(user_id=user.pk)
        assert user.groups.filter().exists() == False
    
        #Set role again
        user_service.set_role(user_id=user.pk, role=GroupEnum.MANAGER.value)
        assert user.groups.first().name == GroupEnum.MANAGER.value

        #Set incorrect role
        with pytest.raises(Exception):
            user_service.set_role(user_id=user.pk, role='some_unexpected_role')