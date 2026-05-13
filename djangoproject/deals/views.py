from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from users.permissions import isDirector, isManager, isAnalyst, isManagerOrDirector
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.authentication import JWTAuthentication

from backend.structures import DealStatus
from accounts.services import AccountService
from contracts.services import ContractService
from .models import Deal
from .serializers import DealGeneralSerializer, DealCloseSerializer, DealItemInputSerializer, DealItemOutputSerializer
from .services import DealService
from users.permissions import isManagerOrDirector
from rest_framework.permissions import AllowAny


# Create your views here.
@extend_schema(tags=['v1_deals'])
class DealViewSet(ModelViewSet):
    serializer_class = DealGeneralSerializer
    authentication_classes= [JWTAuthentication]
    permission_classes = [AllowAny]
    service = DealService(contract_service=ContractService(), account_service=AccountService())
    queryset= Deal.objects.all()
    http_method_names = ['post', 'get', 'put', 'patch'] # No delete

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [isManagerOrDirector()]
        return super().get_permissions()
    
    def get_queryset(self):
        return Deal.objects.select_related('contract', 'account', 'primary_contact') #should be optimized (in service)
    
    def create(self, request, *args, **kwargs):
        '''Open the deal'''
        serializer = DealGeneralSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        deal = self.service.open(**serializer.validated_data)
        serializer = DealGeneralSerializer(deal) # Can change on DealInputSerializer
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(operation_id='v1_deals_close', request=DealCloseSerializer)
    @action(methods=['post'], detail=True)
    def close(self, request, *args, **kwargs):
        '''Close the deal'''
        serializer = DealCloseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        deal = self.service.close(id=kwargs['pk'], **serializer.validated_data)
        serializer = DealGeneralSerializer(deal)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(operation_id='v1_deals_add_deal_item', request=DealItemInputSerializer)
    @action(methods=['post'], detail=True, url_path='items')
    def add_item(self, request, *args, **kwargs):
        '''Add an item to the deal'''
        serializer = DealItemInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        di = self.service.add_item(deal_id=kwargs['pk'], **serializer.validated_data)
        return Response(data=DealItemOutputSerializer(di).data, status=status.HTTP_201_CREATED)

    @extend_schema(operation_id='v1_deals_remove_deal_item', request=None) #specify di_id param to resolve prblms in openapi
    @action(methods=['post'], detail=True, url_path='items/(?P<di_id>[^/.]+)') #capture res into di_id by the rule: seq of chars up to '/' or '.'
    def remove_item(self, request, *args, **kwargs):
        '''Remove an di from the deal (completely)'''
        deal_id, di_id = kwargs['pk'], kwargs['di_id']
        self.service.remove_item(di_id=di_id, deal_id=deal_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @extend_schema(operation_id='v1_deals_update_deal_item', request=DealItemInputSerializer) #specify di_id param to resolve prblms in openapi
    @action(methods=['put'], detail=True, url_path='items/(?P<di_id>[^/.]+)') #capture res into di_id by the rule: seq of chars up to '/' or '.'
    #Add patch too later
    def update_item(self, request, *args, **kwargs):
        '''Remove an di from the deal (completely)'''
        deal_id, di_id = kwargs['pk'], kwargs['di_id']
        self.service.di_repo.update(id=di_id, **kwargs) # bad idea to use repo here. make better later
        return Response(status=status.HTTP_200_OK)