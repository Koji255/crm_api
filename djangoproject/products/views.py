from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from .serializers import CourseGeneralSerializer
from .services import CourseService

# Create your views here
@extend_schema(tags=['v1_products'])
class CourseViewSet(ViewSet):
    service = CourseService()
    serializer_class = CourseGeneralSerializer

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