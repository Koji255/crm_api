from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from users.permissions import isDirector, isManager, isAnalyst, isManagerOrDirector
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from backend.structures import DealStatus
from accounts.services import AccountService
from contracts.services import ContractService
from .models import Deal
from .serializers import DealGeneralSerializer, DealCloseSerializer
from .services import DealService


# Create your views here.
@extend_schema(tags=['v1_deals'])
class DealViewSet(ModelViewSet):
    serializer_class = DealGeneralSerializer
    service = DealService(contract_service=ContractService(), account_service=AccountService())
    queryset= Deal.objects.all()
    http_method_names = ['post', 'get', 'put', 'patch'] # No delete

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [isManagerOrDirector]
        return super().get_permissions()
    
    def get_queryset(self):
        return Deal.objects.select_related('contract_from_deal', 'account_from_deal', 'contact_from_deal') #should be optimized (in service)
    
    def create(self, request, *args, **kwargs):
        '''Open the deal'''
        serializer = DealGeneralSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        deal = self.service.open(**serializer.validated_data)
        serializer = DealGeneralSerializer(deal) # Can change on DealInputSerializer
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True)
    def close(self, request, *args, **kwargs):
        '''Close the deal'''
        serializer = DealCloseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        deal = self.service.close(**serializer.validated_data)
        serializer = DealGeneralSerializer(deal)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
