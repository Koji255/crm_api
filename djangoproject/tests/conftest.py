from typing import List
import pytest
from rest_framework.test import APIClient
from typing import Dict, TypeVar
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from djangoproject.backend.structures import GroupEnum
from users.services import UserService


User = get_user_model()

ServiceType = TypeVar('Service')
UserModel = TypeVar('User')


@pytest.fixture
def client() -> APIClient:
    return APIClient()

@pytest.fixture
def users_model(db) -> Dict[str, UserModel]:
    users = {
        'director1': User.objects.create_user('Jogo', 'somemail1@gmail.com', password='somepasssomepass'),
        'manager1': User.objects.create_user('Jorno', 'somemail2@gmail.com', password='somepasssomepass'),
        'manager2': User.objects.create_user('Jonathan', 'somemail3@gmail.com', password='somepasssomepass'),
        'analyst1': User.objects.create_user('Jotaro', 'somemail4@gmail.com', password='somepasssomepass')
    }
    #set roles to users
    for user_key in users.keys():
        user = users[user_key]
        
        if user_key.startswith('director'):
            group = Group.objects.get(name=GroupEnum.DIRECTOR.value)
            user.groups.set([group])
            
        elif user_key.startswith('manager'):
            group = Group.objects.get(name=GroupEnum.MANAGER.value)
            user.groups.set([group])

        elif user_key.startswith('analyst'):
            group = Group.objects.get(name=GroupEnum.ANALYST.value)
            user.groups.set([group])
    return users

@pytest.fixture
def groups_model(db) -> Group:
    return Group

@pytest.fixture
def services() -> Dict[str, ServiceType]:
    return {
        'user_service': UserService()
    }