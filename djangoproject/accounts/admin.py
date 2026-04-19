from django.contrib import admin
from .models import Account, Contact

# Register your models here.
admin.site.register([Account, Contact])