from django.shortcuts import render
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from users.permissions import isManagerOrDirector, isAnalyst
from rest_framework.permissions import IsAuthenticated
from .models import Contract
from .serializers import ContractGeneralSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.
@extend_schema(tags=['v1_contracts'])
class ContractListRetrieveViewSet(ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    authentication_classes= [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Contract.objects.all()
    serializer_class = ContractGeneralSerializer