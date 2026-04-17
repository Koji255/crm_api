from rest_framework import serializers
# from djoser.serializers import UserSerializer as BaseUserSerializer
from django.contrib.auth.models import User


class RoleInputSerializer(serializers.Serializer):
    role = serializers.CharField(max_length=255)