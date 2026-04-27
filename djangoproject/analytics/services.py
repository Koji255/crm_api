#This best module to practice orm qurs
from decimal import Decimal
from typing import List
from accounts.repos import AccountRepository
from products.repos import CourseRepository
from deals.repos import DealRepository
from contracts.repos import ContractRepository
from backend.structures import DealStatus, CurrencyCode

class AnalyticsService:
    def __init__(self, deal_repo, acc_repo, contract_repo, course_repo):
        self.acc_repo: AccountRepository = acc_repo()
        self.course_repo: CourseRepository = self.course_repo()
        self.deal_repo: DealRepository = deal_repo()
        self.contract_repo: ContractRepository = self.contract_repo()

    def lead_customer_conv_rate(self) -> float:
        '''
        From potential lead (acc created) to a customer\n
        _LCCR = accounts with (at least 1) contracts/all accounts_
        '''
        customer_accs, ttl = self.acc_repo.count_customer_accounts(), self.acc_repo.count_total_accounts()
        return customer_accs / ttl if customer_accs > 0 else 0

    def deal_won_conv_rate(self) -> float:
        '''
        From Deal to Won conversion rate\n
        _DWCR = Won deals/all deals_
        '''
        won, ttl = self.deal_repo.count_won_deals(), self.deal_repo.count_total_deals()
        return won / ttl if won > 0 else 0
    
    def winrate(self):
        # won deals / closed deals
        ...

    def total_pipeline_value(self) -> Decimal:
        '''
        Sum of active deals & contracts (for now in RUB but later make currency conversion)\n
        _TPV = total value of all active delas + ttl val of all active contracts_
        '''
        ttl_active_deals_val, ttl_active_contracts_val = self.deal_repo.total_value_deals(), self.contract_repo.total_value_contracts()
        return sum(ttl_active_deals_val, ttl_active_contracts_val)
    
    def sales_cycle_len(self):
        ...

    def deal_velocity(self):
        # (avg_deal_size * win_rate) / sales_cycle
        ...

    def total_revenue(self) -> Decimal:
        '''Revenue by all time'''
        return self.contract_repo.total_value_contracts()
    
    def new_revenue(self) -> Decimal:
        '''Incoming revenue by the latest minth'''
        return self.contract_repo.total_value_last_month_contracts()
    
    def popular_courses(self, n:int=3) -> List[str]:
        '''Lists names of most purchased courses (courses that has contracts)'''
        return self.course_repo.list_popular_courses(n)