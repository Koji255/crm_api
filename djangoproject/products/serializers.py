from rest_framework import serializers
from .models import Course#, ProductItem

class CourseGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

# class ProductItemOutputSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductItem
#         fields = '__all__'

# class ProductItemInputSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductItem
#         fields = ['quantity', 'course', 'deal'] #contract creates automatically