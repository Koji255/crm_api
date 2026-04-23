from uuid import UUID
from django.db.models import QuerySet
from backend.interfaces import AbstractRepository, BaseRepository
from .models import Contract

class ContractRepository(BaseRepository):
    session = Contract