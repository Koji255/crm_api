from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from users.permissions import isDirector, isManager, isAnalyst, isManagerOrDirector
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from backend.structures import DealStatus
from .serializers import DealGeneralSerializer, DealCloseGeneralSerializer
from .services import DealService

# Create your views here.
@extend_schema(tags=['v1_deals'])
class DealViewSet(ViewSet):
    serializer_class = DealGeneralSerializer
    service = DealService()

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [isManagerOrDirector]
        return super().get_permissions()
    
    def get_queryset(self):
        return self.service.list() #should be optimized (in service)
    
    def list(self, request):
        deals = self.service.list()
        serializer = DealGeneralSerializer(deals, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        deal = self.service.get(deal_id=pk)
        serializer = DealGeneralSerializer(deal)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = DealGeneralSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        deal = self.service.create(serializer.validated_data)
        serializer = DealGeneralSerializer(deal)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        serializer = DealGeneralSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        deal = self.service.update(course_id=pk, **data) #!!
        serializer = DealGeneralSerializer(deal)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    def partial_update(self, request, pk=None):
        serializer = DealGeneralSerializer(data=request.data, partial=True) #!!
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        deal = self.service.update(course_id=pk, **data) #!!
        serializer = DealGeneralSerializer(deal)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    # def destroy(self, request, pk=None):
    
class DealCloseAPIView(APIView):
    permission_classes = [isManagerOrDirector]
    service = DealService()

    def post(self, request, pk):
        #serializer = ... #inplace serializer
        serializer = DealCloseGeneralSerializer(data=request.data)
        deal_status = DealStatus(serializer.data.get('deal_status'))
        loss_reason = serializer.data.get('loss_reason') or None

        updated_deal = self.service.close_deal(deal_id=pk, deal_status=deal_status, loss_reason=loss_reason)
        serializer = DealCloseGeneralSerializer(updated_deal)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
