import uuid
import pytest
from decimal import Decimal
from django.db import transaction
from conftest import users_model, groups_model, courses_model, services
from backend.structures import ProductStatus, DealStatus, AccountStatus
from icecream import ic

from accounts.models import Account as AccountModel
from accounts.services import AccountService
# from products.models import ProductItem as ProductItemModel
from deals.models import Deal as DealModel, DealItem as DealItemModel
from deals.services import DealService
from deals.repos import DealRepository

@pytest.mark.account
class TestAccount:
    def test_update_status(self, accounts_model, deals_model, services):
        acc1 = AccountModel.objects.create(name='accountX', city='New York', address='Quins X')
        acc_service: AccountService = services['account_service']
        deal_service: DealService = services['deal_service']
        # Account status by defauly
        assert acc1.status == AccountStatus.NEW
        # ic(acc1.status)

        #Open new deal on acc & check that status updated
        deal = deal_service.open(account_id=acc1.pk)
        acc_service.update_status(id=acc1.pk)
        acc1.refresh_from_db()
        assert acc1.status == AccountStatus.LEAD
        # ic(acc1.status)

        deal_service.close(id=deal.id, status=DealStatus.LOST)
        acc_service.update_status(id=acc1.pk)
        acc1.refresh_from_db()
        assert acc1.status == AccountStatus.ACTIVE
        # ic(acc1.status)