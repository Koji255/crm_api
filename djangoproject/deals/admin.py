from django.contrib import admin
from .models import Deal, DealItem

# Register your models here.
admin.site.register((Deal, DealItem))