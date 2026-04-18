from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema

from users.permissions import isAnalyst, isManager, isDirector, isManagerOrDirector
from .models import Account, Contact
from .serializers import AccountGeneralSerializer, ContactGeneralSerializer

# Create your views here.
@extend_schema(tags=['v1_accounts'])
class AccountModelViewSet(viewsets.ModelViewSet):
    permission_classes = [isManagerOrDirector]
    serializer_class = AccountGeneralSerializer
    queryset = Account.objects.all()

@extend_schema(tags=['v1_contacts'])
class ContactModelViewSet(viewsets.ModelViewSet):
    permission_classes = [isManagerOrDirector]
    serializer_class = ContactGeneralSerializer
    queryset = Contact.objects.all()