import uuid
from backend.structures import GroupEnum
# from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from .models import UserNotFound

User = get_user_model()

class UserService:
    '''No repo for now'''
    #later when tasks and notes will come up this service layer will be usefull
    # def __init__(self, user_id: uuid.UUID):
    #     self.user = User.objects.get(pk=user_id)
    def _get_user(self, user_id) -> AbstractUser:
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist as e:
            raise UserNotFound(f'{UserNotFound.MSG}\nDetails:{e}')
    
    def set_role(self, user_id: uuid.UUID, role: str) -> None:
        user = self._get_user(user_id)
        user.set_role(role)

    def revoke_role(self, user_id: uuid.UUID) -> None:
        user = self._get_user(user_id)
        user.revoke_role()

    def get_role(self, user_id: uuid.UUID) -> str:
        user = self._get_user(user_id)
        return user.get_role