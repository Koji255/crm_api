from rest_framework import serializers
from .models import Contract

class ContractGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'