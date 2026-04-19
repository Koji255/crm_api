from uuid import uuid4
from django.db import models

# Create your models here.
class Deal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
