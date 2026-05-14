import pytest
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any
from rest_framework.test import APIClient
from icecream import ic
from backend.structures import DealStatus

@dataclass(frozen=True)
class Param:
    account: Dict[str, Any]
    contact: Dict[str, Any] = field(default_factory=dict)
    deal:  Dict[str, Any] = field(default_factory=dict)
    # contract: dict[str, object] = field(default_factory=dict)
    is_edge_case: bool=False #most important thing.With this flag it's possible to split method into deviant & stable use-cases

    def account_created(self, account_id):
        self.contact['account'] = account_id
        self.deal['account'] = account_id
    
    def contact_created(self, contact_id):
        self.deal['primary_contact'] = contact_id

@pytest.mark.e2e
@pytest.mark.pipeline
class TestPipeline:
    main_pipeline_params: List[Param] = [
        Param(
            account={
                'name': 'Test Account',
                'city': 'Los Angeles',
                'address': 'Sunset Blvd 1',
                'description': 'Test account description'
            },
            contact={
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@example.com',
                # 'phone': '+10000000000',
                'phone': None,
                'account': None # must be updated after account post
            },
            deal={
                # 'status': 'open',
                # 'expected_value': '1000.00', #!!
                # 'expected_close_date': '2026-06-01',
                'description': 'Test deal description',
                # 'loss_reason': None,
                # 'closed_at': None
                'account': None, # must be updated after account post
                'primary_contact': None # # must be updated after contact post
            },
            # contract={
            #     'deal': None #Must be updated after deal creation
            # },
            is_edge_case=False
        ),
        #Param2(...
    ]

    @pytest.mark.parametrize('param', main_pipeline_params)
    def test_main_pipeline(self, fa_client: APIClient, param: Param, courses_model):
        '''
        Pipeline:
        Create Account -> Create Contact from account -> Create Deal from account <open_deal> -> Create Contract from deal <open_contract>
        '''
        course_id = courses_model['course1'].pk

        # Create an Account
        acc_post_rsp = fa_client.post(
            path='/api/v1/accounts/',
            format='json',
            data=param.account # this is beatifull
        )
        assert acc_post_rsp.status_code == 201; ic(acc_post_rsp.data)
        acc_id = acc_post_rsp.data['id']#; ic(acc_id)
        param.account_created(account_id=acc_id) #get account id & set it to the future objs for post qur

        # Create a Contact
        cntct_post_rsp = fa_client.post(
            path='/api/v1/contacts/',
            format='json',
            data=param.contact
        )
        assert cntct_post_rsp.status_code == 201; ic(cntct_post_rsp.data)
        cntct_id = cntct_post_rsp.data['id']
        param.contact_created(contact_id=cntct_id)

        # Open a Deal
        deal_post_rsp = fa_client.post(
            path='/api/v1/deals/',
            format='json',
            data=param.deal
        )
        assert deal_post_rsp.status_code == 201; ic(deal_post_rsp.data)
        deal_id = deal_post_rsp.data['id']

        # Close the deal as WON & open a contract from this deal
        deal_close_won_rsp = fa_client.post(
            path=f'/api/v1/deals/{deal_id}/close/',
            format='json',
            data={
                'status': DealStatus.WON
            }
        )
        assert deal_close_won_rsp.status_code == 200; ic(deal_close_won_rsp.data)
        assert deal_close_won_rsp.data['status'] == DealStatus.WON
        assert deal_close_won_rsp.data['contract'] is not None