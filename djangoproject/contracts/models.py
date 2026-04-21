from uuid import uuid4
from django.db import models

class ContractNotFound(Exception):
    MSG = 'Object with given id does not exist'

# Create your models here.
class Contract(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
