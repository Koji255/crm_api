import uuid
from typing import List
from decimal import Decimal
from django.db.models import QuerySet, F, Sum, DecimalField
from django.db import transaction
from django.db.utils import IntegrityError

from backend.structures import DealStatus
from products.models import Course#, ProductItem
# from products.services import ProductItemService
from .models import Deal, DealNotFound, DealNotAvailable

class DealService():
    def _make_title(self, deal_id: uuid.UUID, account_name: str, owner_username: str) -> str:
        # products: List[str] = list(Course.objects.filter(created_productitems__deal_id=deal_id).values_list('name', flat=True))
        res = [f'id:{str(deal_id)[:8]}', f'account:{account_name}', f'owner:{owner_username}']
        # if not products:
        #     res.append(f'products:"NO_PRODUCTS"')
        # else:
        #     res.append(f'products:"{products}"')
        return '::'.join(res)

    def _make_expected_value(self, deal_id: uuid.UUID) -> Decimal:
        '''from ProductItem sum of products of 2 columns from join with Course'''
        result = Deal.objects.filter(id=deal_id).aggregate(
            total = Sum(
                F('included_productitems__course__unit_price') * F('included_productitems__quantity'),
                output_field=DecimalField()
            )
        )
        # print(f'DEBUGGGGGGIIIING: {result['total']}')
        return result['total'] or Decimal('0')

    def _get_deal(self, deal_id: uuid.UUID) -> Deal:
        '''
        Returns Course model object. Later replace with dto
        '''
        try:
            deal = Deal.objects.get(pk=deal_id)
            #This is a shortcut cuz I'm lazy enough to redefine ProductItem viewset
            #Later call it only in PI vs, NOT IN GET FUNCTION
            #this solution is distructive for performance
            deal.expected_value = self._make_expected_value(deal_id=deal.pk) #OPTIMIZE IT LATER!!!!!!
        except Deal.DoesNotExist as e:
            raise DealNotFound(f'{DealNotFound.MSG}\nDetails:{e}')
        return deal
    
    def validate_deal(self, deal_id: uuid.UUID):
        '''
        Raises *DealNotAvailable* Exception if deal is not available.\n
        Validates: *deal.is_open*
        '''
        with transaction.atomic():
            deal = self._get_deal(deal_id=deal_id) 
            if not deal.is_open:
                raise DealNotAvailable(f'{DealNotAvailable.MSG}') # Add logic to manually select first available deal or create new one

    def close_deal(self, deal_id: uuid.UUID, deal_status: DealStatus, loss_reason: str=None)-> Deal:
        from contracts.services import ContractService

        with transaction.atomic():
            deal = self._get_deal(deal_id)
            deal.status = deal_status
            if deal.status in (DealStatus.LOST, DealStatus.ARCHIVED):
                deal.loss_reason = loss_reason
            elif deal.status == DealStatus.WON:
                contract_service = ContractService()
                # contract = contract_service.create(deal_id=deal.id) # add to dto
            deal.save()

            return deal # to return contract info with deal, migrate to dto

    def list(self) -> QuerySet:
        return Deal.objects.all().prefetch_related('included_productitems__course')

    def create(self, **kwargs) -> Deal:
        '''Later will return dto instead of model'''
        try:
            deal = Deal(**kwargs)
            if not deal.title:
                deal.title = self._make_title(deal_id=deal.pk, account_name=deal.account.name, owner_username=deal.owner.username)
            deal.save()
        except IntegrityError as e:
           raise ValueError(f'Cannot create a deal with such params\nkwargs{kwargs}\nDetails: \n{e}')
        return deal

    def get(self, deal_id: uuid.UUID) -> Deal:
        # a bit weird
        return self._get_deal(deal_id)
    
    def update(self, deal_id: uuid.UUID, **kwargs) -> Deal:
        '''Returns updated version of deal'''
        with transaction.atomic():
            deal = self._get_deal(deal_id)
            for field, val in kwargs.items(): #New ver. of update
                setattr(deal, field, val)
            deal.save()
            return deal.refresh_from_db()


    def delete(self, deal_id: uuid.UUID): 
        pass
        #     '''Course can be removed if & only if it has no relations in deals & contracts.\nElse only status will be changed (on archieved)'''
        #     with transaction.atomic():
        #         #Try for idempotency
        #         try:
        #             course = self._get_course(course_id=course_id) #Race risk
        #             if course.has_relations:
        #                 course.status = ProductStatus.ARCHIVED # make update logic
        #                 course.save(); status = course.status
        #             else:
        #                 course.delete(); status = ProductStatus.DELETED
        #         except DealNotFound:
        #             status = ProductStatus.DELETED
        #         return status