import pytest
from icecream import ic
from decimal import Decimal
from backend.structures import COUNTRIES
from accounts.models import Account
from products.models import Course
from deals.models import Deal, DealItem
from contracts.models import Contract
from analytics.services import AnalyticsService
from deals.repos import DealRepository, DealItemRepository
from accounts.repos import AccountRepository
from contracts.repos import ContractRepository
from products.repos import CourseRepository
#Trash. make normal tests via services

@pytest.mark.analytics
@pytest.mark.django_db
class TestAnalytics:
    def test_total_revenue(self):
        service = AnalyticsService(
            deal_repo=DealRepository,
            acc_repo=AccountRepository,
            contract_repo=ContractRepository,
            course_repo=CourseRepository
        )
        account = Account.objects.create(name='accountX', country=COUNTRIES[0][0], city='Moscow', address='addressX')
        course = Course.objects.create(name='courseX', unit_price=Decimal('25'))
        deal = Deal.objects.create(account_id=account.pk)
        di = DealItem.objects.create(course_id=course.pk, deal_id=deal.pk)
        contract = Contract.objects.create()
        deal.contract = contract #!

        ttl_rev = service.total_revenue()
        ic(ttl_rev)
        # assert ttl_rev > Decimal('0')