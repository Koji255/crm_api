from enum import Enum
from django.db.models import TextChoices # mb upgrade on textchoices later

# GROUPS = set('Director', 'Manager', 'Analyst')
class GroupEnum(Enum):
    DIRECTOR = 'director'
    MANAGER = 'manager'
    ANALYST = 'analyst'

ACCOUNT_TYPES = [
    ('SCHOOL', 'school'),
    ('UNIVERSITY', 'university'),
    ('COMPANY', 'company'),
    ('OTHER', 'other')
]

ACCOUNT_STATUSES = [
    '''Most dynamic BR'''
    ('NEW', 'new'), # account has no leads & contracts
    #Lead higher than customer (if active contracts & active leads, status will be lead)
    ('LEAD', 'lead'), #account will be lead if there are at least 1 opened leading procedureю. So this is client with interest
    #if account tried to make a lead & failed it also becoms a customer
    ('CUSTOMER', 'customer'), #if account has only contracts (active or inactive) & no leads 
    # ('LOST', 'lost')
]

COUNTRIES = [ #I need functionality to extend this list manually (for director)
    ('RUSSIA', 'russia'), #Theese are countries where our company work
    ('BELARUS' 'belarus'),
    ('KAZAKHSTAN', 'kazakhstan'),
    ('USA', 'usa'),
    ('OTHER', 'other')
]