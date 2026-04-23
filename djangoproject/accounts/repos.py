from uuid import UUID
from django.db.models import QuerySet
from backend.interfaces import AbstractRepository, BaseRepository
from .models import Account

class AccountRepository(BaseRepository):
    session = Account