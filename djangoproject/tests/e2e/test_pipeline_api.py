import pytest
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any
from rest_framework.test import APIClient
from icecream import ic

@dataclass(frozen=True)
class Param:
    account: Dict[str, Any]
    contact: Dict[str, Any] = field(default_factory=dict)
    deal:  Dict[str, Any] = field(default_factory=dict)
    # contract: dict[str, object] = field(default_factory=dict)
    is_edge_case: bool=False #most important thing.With this flag it's possible to split method into deviant & stable use-cases

@pytest.mark.e2e
@pytest.mark.pipline
class TestPipeline:
    main_pipeline_params: List[Param] = [
        Param(
            account={
                'name': 'Test Account',
                'city': 'Los Angeles',
                'address': 'Sunset Blvd 1',
                'description': 'Test account description',
            },
            contact={
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@example.com',
                'phone': '+10000000000',
            },
            deal={
                'status': 'open',
                'expected_value': '1000.00',
                'expected_close_date': '2026-06-01',
                'description': 'Test deal description',
                'loss_reason': None,
                'closed_at': None,
            },
            # contract={
            #     'status': 'active',
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

        acc_post_rsp = fa_client.post(
            path='/api/v1/accounts/',
            format='json',
            data=param.account # this is beatifull
        )
        assert acc_post_rsp.status_code == 201; ic(acc_post_rsp.data)
        