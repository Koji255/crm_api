from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema

from users.permissions import isAnalyst, isManager, isDirector, isManagerOrDirector
from .models import Account, Contact
from .serializers import AccountGeneralSerializer, ContactGeneralSerializer

from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.
@extend_schema(tags=['v1_accounts'])
class AccountModelViewSet(viewsets.ModelViewSet):
    # authentication_classes = [JWTAuthentication]
    permission_classes = [isManagerOrDirector,]
    serializer_class = AccountGeneralSerializer
    queryset = Account.objects.prefetch_related('contacts_from_account') # for list of qs in serializer
    # def list(self, request, *args, **kwargs):
    #     print("USER:", request.user)
    #     print("AUTH:", request.auth)
    #     return super().list(request, *args, **kwargs)

@extend_schema(tags=['v1_contacts'])
class ContactModelViewSet(viewsets.ModelViewSet):
    # authentication_classes = [JWTAuthentication]
    permission_classes = [isManagerOrDirector]
    serializer_class = ContactGeneralSerializer
    queryset = Contact.objects.all()