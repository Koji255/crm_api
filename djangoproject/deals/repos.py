from uuid import UUID
from backend.interfaces import AbstractRepository
from .models import Deal

class DealRepository(AbstractRepository):
    def __init__(self):
        self.session = Deal