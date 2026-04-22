import uuid
from typing import List
from decimal import Decimal
from django.db import transaction
from django.db.utils import IntegrityError
from django.utils.timezone import datetime
from django.db.models import QuerySet, F, Sum, DecimalField

from backend.structures import DealStatus
from products.models import Course#, ProductItem
# from products.services import ProductItemService
from .models import Deal, DealNotFound, DealNotAvailable
from .repos import DealRepository

class DealService():
    def __init__(self):
        self.deal_repo = DealRepository()

    def _get_deal(self, id: uuid.UUID) -> Deal:
        '''Returns Course model object. Later replace with dto'''
        try:
            return Deal.objects.get(pk=id)
        except Deal.DoesNotExist as e:
            raise DealNotFound(f'{DealNotFound.MSG}\nDetails:{e}')

    def get_exp_val(self, id: uuid.UUID) -> Decimal:
        '''from DealItem sum of products of 2 columns from join with Course'''
        with transaction.atomic():
            result = Deal.objects.filter(pk=id).aggregate(
                total = Sum(
                    F('di_from_deal__course__unit_price') * F('di_from_deal__quantity'), # add discount
                    output_field=DecimalField()
                )
            )
            return result['total']

    def close_deal(self, id: uuid.UUID, status: DealStatus=DealStatus.WON, loss_reason: str|None=None):
        # if status in (DealStatus.LOST, DealStatus.ARCHIVED):
        n = self.deal_repo.update(id=id, status=status, loss_reason=loss_reason, closed_at=datetime.now())
        if n == 0: raise DealNotFound(f'{DealNotFound.MSG}')

    def add_item(self):
        ...

    def remove_item(self):
        ...