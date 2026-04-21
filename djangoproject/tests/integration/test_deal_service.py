import uuid
import pytest
from decimal import Decimal
from conftest import users_model, groups_model, courses_model, services
from backend.structures import ProductStatus
from icecream import ic

from accounts.models import Account as AccountModel
from products.models import ProductItem as ProductItemModel
from deals.models import Deal as DealModel
from deals.services import DealService

@pytest.mark.deal
class TestDeal:
    def test_deal_crud(self, users_model, courses_model, deals_model, productitems_model, services):
        deal_service: DealService = services['deal_service']
        account = AccountModel.objects.create(name='accountX', city='New York', address='Quins 7')
        owner = users_model['manager2']

        # Try to create new deal with title auto generation
        deal = deal_service.create(account_id=account.pk, owner_id=owner.pk)
        assert deal.expected_value == 0.0
        assert DealModel.objects.filter(account_id=account.pk).exists()
        assert DealModel.objects.filter(account_id=account.pk).count() == 1
        #_make_title validation (format: id[:8]::account.name::owner.username)
        assert deal.title.endswith(owner.first_name)
        assert account.name in deal.title
        # ic(deal.title)

        # No idempotency. Can create new deal with same 'open' status
        deal = deal_service.create(account_id=account.pk, owner_id=owner.pk)
        assert DealModel.objects.filter(account_id=account.pk).count() == 2
        #_make_title validation (format: id[:8]::account.name::owner.username)
        assert deal.title.endswith(owner.first_name)
        # ic(deal.title)
        
        #Invalid id
        with pytest.raises(Exception):
            deal_service.create(account_id='nope')

        assert deal.expected_value == Decimal('0')
        
        #Rebuild PI from VS to apiview + services, in order to test pi in integration tests properly
        pi1 = ProductItemModel.objects.create(course=courses_model['course1'], deal=deal, quantity=1)
        pi2 = ProductItemModel.objects.create(course=courses_model['course2'], deal=deal, quantity=1)

        expected_value = deal_service._make_expected_value(deal.pk)
        deal_service.update(deal.id, expected_value=expected_value)

        deal.refresh_from_db()
        assert deal.expected_value > Decimal('0')
        # ic(pi1); ic(pi2); ic(deal.expected_value)