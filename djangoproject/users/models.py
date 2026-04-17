from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from phonenumber_field.modelfields import PhoneNumberField

from backend.enums import GroupEnum

# Create your models here.
class User(AbstractUser):
    #Users are only university's staff. They manage all things in crm, while accounts are just counterparties, that have no access to the crm
    #All other fields extends from djoser's user model
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    phone_number = PhoneNumberField(verbose_name='phone_number', blank=True, null=True, default=None)

    def __str__(self):
        return f'{self.id}: {self.username} | Role: {self.groups.first()}'
    
    @property
    def get_role(self) -> str:
        group = self.groups.first()
        return group.name if group else None
    
    @property
    def has_role(self, name: str) -> bool:
        group = self.groups.first()
        return group.name == name

    def set_role(self, role_name: str) -> None:
        try:
            group = Group.objects.get(name=role_name)
        except Group.DoesNotExist:
            raise ValueError(f'Group {role_name} does not exist')
        
        self.groups.set([group]) #fix it later. Groups - m2m relationship. BR - 1 group to 1 user

    def revoke_role(self) -> None:
        self.groups.clear()