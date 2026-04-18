from rest_framework import serializers
from .models import Account, Contact

class ContactGeneralSerializer(serializers.ModelSerializer):
    #serializers devided in 3 categories: Input, Output & General
    class Meta:
        model = Contact
        fields = '__all__'

class AccountGeneralSerializer(serializers.ModelSerializer):
    #serializers devided in 3 categories: Input, Output & General
    contacts = ContactGeneralSerializer(many=True, read_only=True) # includes contacts list in this serializer
    class Meta:
        model = Account
        fields = '__all__'