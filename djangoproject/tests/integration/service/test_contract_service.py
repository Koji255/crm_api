import pytest
from datetime import timedelta
from django.utils import timezone
from deals.models import DealItem as DealItemModel
from accounts.models import Account as AccountModel, Contact as ContactModel
from contracts.services import ContractService

@pytest.mark.contract
@pytest.mark.prod_db
class TestContract:
    def test_contract_open(self, users_model, courses_model, services):
        contract_service: ContractService = services['contract_service']
        deal_service = services['deal_service']
        account = AccountModel.objects.create(
            name='accountX',
            city='New York',
            address='Quins 7'
        )
        contact = ContactModel.objects.create(first_name='Somename', email='someemail@gmail.com', account_id=account.pk) #!
        owner = users_model['manager2']
        #New deal
        deal = deal_service.open(account_id=account.pk, owner_id=owner.pk, primary_contact_id=contact.pk)#!
        # dealitem & access_months
        di = DealItemModel.objects.create(
            deal=deal,
            course=courses_model['course1'],
            quantity=1,
            access_months=2
        )

        # Act
        contract = contract_service.open(deal_id=deal.pk)
        # Refresh
        di.refresh_from_db()
        
        today = timezone.now().date()
        # Assert: контракт создан
        assert contract is not None
        assert contract.deal_from_contract.pk == deal.pk

        # Assert: даты проставлены
        assert di.start_date == today

        expected_end = today + timedelta(weeks=2 * 4)
        assert di.end_date == expected_end