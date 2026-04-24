import uuid
import pytest
from decimal import Decimal
from django.db import transaction
from conftest import users_model, groups_model, courses_model, services
from backend.structures import ProductStatus, DealStatus
from icecream import ic

from accounts.models import Account as AccountModel
# from products.models import ProductItem as ProductItemModel
from deals.models import Deal as DealModel, DealItem as DealItemModel
from deals.services import DealService
from deals.repos import DealRepository

@pytest.mark.deal
class TestDeal:
    def test_deal_open_close(self, users_model, courses_model, deals_model, dealitems_model, services, repos):
        deal_service: DealService = services['deal_service']
        deal_repo: DealRepository = repos['deal_repo']
        account = AccountModel.objects.create(name='accountX', city='New York', address='Quins 7')
        owner = users_model['manager2']

        # Try to create new deal with title auto generation
        deal = deal_service.open(account_id=account.pk, owner_id=owner.pk)
        assert deal.expected_value == Decimal('0')
        assert DealModel.objects.filter(account_id=account.pk).exists()
        assert DealModel.objects.filter(account_id=account.pk).count() == 1

        # No idempotency. Can create new deal with same 'open' status
        deal = deal_service.open(account_id=account.pk, owner_id=owner.pk)
        assert DealModel.objects.filter(account_id=account.pk).count() == 2
        #_make_title validation (format: id[:8]::account.name::owner.username)
        # assert deal.title.endswith(owner.first_name)
        # ic(deal.title)
        
        #Invalid id
        with pytest.raises(Exception):
            with transaction.atomic():
                deal_service.open(account_id='nope')

        assert deal.expected_value == Decimal('0')
        
        #ADD DEALITEM & REMOVE DEALITEM
        #Rebuild PI from VS to apiview + services, in order to test pi in integration tests properly
        di1 = dealitems_model['dealitem1']
        di2 = dealitems_model['dealitem2']

        # expected_value = deal_service._make_expected_value(deal.pk)
        # deal_repo.update(deal.id, expected_value=expected_value)
        deal_service.add_item(deal_id=deal.pk, di_id=di1.pk)
        deal.refresh_from_db()
        assert deal.expected_value > Decimal('0')
        # ic(di1); ic(di2); ic(deal.expected_value)

        deal_service.add_item(deal_id=deal.pk, di_id=di2.pk)
        deal.refresh_from_db()
        assert deal.expected_value == (di1.course.unit_price * di1.quantity * di1.access_months) + (di2.course.unit_price * di2.quantity * di2.access_months)
        # ic(di1); ic(di2); ic(deal.expected_value)

        # Close deal without contract module
        #must update status field
        assert deal.status == 'open'
        # ic(deal.status)
        deal_service.close(id=deal.pk, status=DealStatus.WON)
        deal.refresh_from_db()
        assert deal.status == DealStatus.WON
        # ic(deal.status)
        