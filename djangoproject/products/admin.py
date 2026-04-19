from django.contrib import admin
from .models import Course, ProductItem

# Register your models here.
admin.site.register([Course, ProductItem])