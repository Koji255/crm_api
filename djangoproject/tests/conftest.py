from typing import List
import pytest
from rest_framework.test import APIClient
from typing import Dict, TypeVar
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from backend.structures import GroupEnum
from users.services import UserService
from products.services import CourseService#, ProductItemService
from products.repos import CourseRepository#, ProductItemRepository
from products.models import Course as CourseModel#, ProductItem as ProductItemModel
from deals.models import Deal as DealModel, DealItem as DealItemModel
from deals.repos import DealRepository, DealItemRepository
from deals.services import DealService
from accounts.models import Account as AccountModel
from accounts.services import AccountService
from contracts.services import ContractService


User = get_user_model()

ServiceType = TypeVar('Service')
RepoType = TypeVar('Repo')
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
def courses_model(db) -> Dict[str, CourseModel]:
    courses = {
        'course1': CourseModel.objects.create(name='Course1', unit_price=25.00),
        'course2': CourseModel.objects.create(name='Course2', unit_price=1500.00)
    }
    return courses

@pytest.fixture
def accounts_model(db) -> Dict[str, AccountModel]:
    accounts = {
        'account1': AccountModel.objects.create(name='account1', city='New York', address='Quins 5'),
        'account2': AccountModel.objects.create(name='account2', city='New York', address='Quins 6')
    }
    return accounts

@pytest.fixture
def deals_model(db, users_model, accounts_model) -> Dict[str, DealModel]:
    deals = {
        'deal1': DealModel.objects.create(account=accounts_model['account1'], owner=users_model['manager1']),
        'deal2': DealModel.objects.create(account=accounts_model['account2'], owner=users_model['manager1'])
    }
    return deals

@pytest.fixture
def dealitems_model(db, courses_model, deals_model) -> Dict[str, DealItemModel]:
    productitems = {
        'dealitem1': DealItemModel.objects.create(course=courses_model['course1'], deal=deals_model['deal1']),
        'dealitem2': DealItemModel.objects.create(course=courses_model['course2'], deal=deals_model['deal1'], access_months=3)
    }
    return productitems

@pytest.fixture
def repos() -> Dict[str, RepoType]:
    return {
        'course_repo': CourseRepository(),
        'deal_repo': DealRepository(),
        'di_repo': DealItemRepository()
    }

@pytest.fixture
def services() -> Dict[str, ServiceType]:
    return {
        'user_service': UserService(),
        'account_service': AccountService(),
        'course_service': CourseService(),
        'deal_service': DealService(),
        # 'di_service': DealIte(),
        'contract_service': ContractService()
    }