from django.shortcuts import render
from rest_framework.views import APIView, View
from rest_framework.generics import api_settings
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from .permissions import isDirector, isManager, isAnalyst
from .serializers import RoleInputSerializer
from .services import UserService

# Create your views here
class RoleAPIView(APIView):
    permission_classes = [isDirector]
    service = UserService()
    serializer_class = RoleInputSerializer # Later implement General serializer.

    @extend_schema(request=RoleInputSerializer, summary='v1_set_role')
    def put(self, request, pk):
        serializer = RoleInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.service.set_role(pk, serializer.validated_data['role'])
        return Response(data={'status': f'role updated to {self.service.get_role(pk)}'}, status=status.HTTP_200_OK)
    
    @extend_schema(summary='v1_revoke_role')
    def delete(self, request, pk):
        self.service.revoke_role(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)