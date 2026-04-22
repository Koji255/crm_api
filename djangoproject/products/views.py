from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from users.permissions import isDirector, isManager, isAnalyst, isManagerOrDirector
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from drf_spectacular.utils import extend_schema

from .models import ProductItem
from .services import CourseService
from products.services import ProductItemService
from .serializers import CourseGeneralSerializer, ProductItemGeneralSerializer
from deals.services import DealService

# Create your views here
class CourseWebHooks:
    @api_view(http_method_names=['POST'])
    def create_course_api_view(self, request):
        pass
    @api_view(http_method_names=['PUT'])
    def update_course_api_view(self, request):
        pass
    @api_view(http_method_names=['DELETE'])
    def delete_course_api_view(self, request):
        pass

@extend_schema(tags=['v1_products'])
class CourseViewSet(ViewSet):
    serializer_class = CourseGeneralSerializer
    service = CourseService()

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [isManagerOrDirector]
        return super().get_permissions()
    
    def get_queryset(self):
        return self.service.list()
    
    def list(self, request):
        courses = self.service.list()
        serializer = CourseGeneralSerializer(courses, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        course = self.service.get(course_id=pk)
        serializer = CourseGeneralSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = CourseGeneralSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course = self.service.create(serializer.validated_data)
        serializer = CourseGeneralSerializer(course)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        serializer = CourseGeneralSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        course = self.service.update(course_id=pk, **data) #!!
        serializer = CourseGeneralSerializer(course)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    def partial_update(self, request, pk=None):
        serializer = CourseGeneralSerializer(data=request.data, partial=True) #!!
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        course = self.service.update(course_id=pk, **data) #!!
        serializer = CourseGeneralSerializer(course)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        product_status = self.service.delete(course_id=pk)
        return Response({"product_status": product_status}, status=status.HTTP_200_OK)

# @extend_schema(tags=['v1_product_items'])
# class ProductItemModelViewSet(ModelViewSet): # migrate to service layer cuz too much logic
#     '''Add make_title on post'''
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     serializer_class = ProductItemGeneralSerializer
#     deal_service = DealService()
#     queryset = ProductItem.objects.all()

#     def perform_create(self, serializer):
#         inst = serializer.save()
#         self.deal_service.add_to_deal(deal_id=inst.deal_id, pi_id=inst.id)
#         # expected_value = self.deal_service.make_expected_value(deal_id=deal_id)
#         # self.deal_service.update(deal_id, expected_value=expected_value)

#     # def perform_update(self, serializer):
#     #     pi = serializer.save()
#     #     deal_id = pi.deal_id
#     #     expected_value = self.deal_service.make_expected_value(deal_id=deal_id)
#     #     self.deal_service.update(deal_id, expected_value=expected_value)
@extend_schema(tags=['v1_product_items'])
class ProductItemViewSet(ModelViewSet):
    serializer_class = ProductItemGeneralSerializer
    service = ProductItemService()

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [isManagerOrDirector()]
        return super().get_permissions()
    
    def get_queryset(self):
        return self.service.list()
    
    def create(self, request):
        serializer = ProductItemGeneralSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pi = self.service.create(serializer.validated_data) # Extra logic inside the service
        serializer = ProductItemGeneralSerializer(pi)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    # def retrieve(self, request, pk=None):
    #     pi = self.service.get(pi_id=pk)
    #     serializer = ProductItemGeneralSerializer(pi)
    #     return Response(serializer.data, status=status.HTTP_200_OK)