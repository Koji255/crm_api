from rest_framework import serializers
from backend.structures import DealStatus
from .models import Deal, DealItem


class DealGeneralSerializer(serializers.ModelSerializer):
    #acc
    #contract
    #main_contact
    class Meta:
        model = Deal
        fields = '__all__'

class DealCloseSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=DealStatus.choices)
    loss_reason = serializers.CharField(required=False, allow_null=True, allow_blank=True)

class DealItemOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealItem
        fields = '__all__'

class DealItemInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealItem
        fields = ['quantity', 'course']#, 'deal'] #get deal from url args