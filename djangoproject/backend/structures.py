from enum import Enum
from django.db.models import TextChoices # mb upgrade on textchoices later
from django.db import models

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

# ACCOUNT_STATUSES = [
#     #Most dynamic BR
#     #Contract is a won deal
#     ('NEW', 'new'), # account has no leads & contracts
#     ('ACTIVE', 'active'), # if account has no contracts but have tried to open a deal (but it lost), he will become an active
#     #Lead higher than customer (if active contracts & active deals, status will be lead)
#     ('LEAD', 'lead'), #account will be lead if there are at least 1 opened deal procedure. So this is a client with the interest
#     #if account tried to make a lead & failed it also becoms a customer
#     ('CUSTOMER', 'customer'), #if account has only contracts (active or inactive) & no leads 
#     # ('LOST', 'lost')
# ]
class AccountStatus(models.TextChoices):
    # changed brs: now customer is above the lead
    NEW = 'new', 'New'
    ACTIVE = 'active', 'Active'
    CUSTOMER = 'customer', 'Customer'
    LEAD = 'lead', 'Lead'

COUNTRIES = [ #I need functionality to extend this list manually (for director)
    ('RUSSIA', 'russia'), #Theese are countries where our company work
    ('BELARUS', 'belarus'),
    ('KAZAKHSTAN', 'kazakhstan'),
    ('USA', 'usa'),
    ('EUROPE', 'europe'),
    ('OTHER', 'other')
]

class CurrencyCode(models.TextChoices):
    USD = 'USD', 'dollar'
    RUB = 'RUB', 'ruble'

class ProductStatus(models.TextChoices):
    ACTIVE = 'active', 'Active',
    ARCHIVED = 'archived', 'Archived'
    DELETED = 'deleted', 'Deleted'

class DealStatus(models.TextChoices):
    OPEN = 'open', 'Open'
    WON = 'won', 'Won'
    LOST = 'lost', 'Lost'
    ARCHIVED = 'archived', 'Archived'

class ContractStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    EXPIRED = 'expired', 'Expired'