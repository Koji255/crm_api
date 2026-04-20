import uuid
from typing import List
from decimal import Decimal
from django.db.models import QuerySet, F, Sum, DecimalField
from django.db import transaction
from django.db.utils import IntegrityError
from products.models import Course
from .models import Deal, DealNotFound


class DealService():
    def _make_title(self, deal_id: uuid.UUID, account_name: str) -> str:
        hash_ = str(deal_id)[:8]
        products: List[str] = list(Course.objects.filter(created_productitems__deal_id=deal_id).values_list('name', flat=True))
        res = [f'id:"{hash_}..."', f'account:"{account_name}"']
        if not products:
            res.append(f'products:"NO_PRODUCTS"')
        else:
            res.append(f'products:"{products}"')
        return '::'.join(res)

    def _make_expected_value(self, deal_id: uuid.UUID) -> Decimal:
        '''from ProductItem sum of products of 2 columns from join with Course'''
        result = Deal.objects.filter(id=deal_id).aggregate(
            total = Sum(
                F('included_productitems__course__unit_price') * F('included_productitems__quantity'),
                output_field=DecimalField()
            )
        )
        print(f'DEBUGGGGGGIIIING: {result['total']}')
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
            # deal.expected_value = self.make_expected_value(deal_id=deal.pk) #REPLACE IT LATER!!!!!!
        except Deal.DoesNotExist as e:
            raise DealNotFound(f'{DealNotFound.MSG}\nDetails:{e}')
        return deal

    def list(self) -> QuerySet:
        return Deal.objects.all()

    def create(self, **kwargs) -> Deal:
        '''Later will return dto instead of model'''
        try:
            deal = Deal(**kwargs)
            if not deal.title:
                deal.title = self.make_title(deal.pk, deal.account.name)
            deal.save()
        except IntegrityError as e:
           raise ValueError(f'Cannot create a deal with such params\nkwargs{kwargs}\nDetails: \n{e}')
        return deal

    def get(self, deal_id: uuid.UUID) -> Course:
        # a bit weird
        return self._get_deal(deal_id)
    
    def update(self, deal_id: uuid.UUID, **kwargs) -> Deal:
        '''Returns amount of rows affected by an update method'''
        with transaction.atomic():
            deal = Deal.objects.filter(pk=deal_id)
            if not deal.exists():
                raise DealNotFound(f'{DealNotFound.MSG}\nID: {deal_id}')
            deal.update(**kwargs)
            return deal.first()
        
    def close_deal(self, *args):
        pass
    
    def delete(self, deal_id: uuid.UUID): 
        ... 
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