import uuid
from backend.enums import GroupEnum
from .models import User

class UserService:
    '''No repo for now'''
    #later when tasks and notes will come up this service layer will be usefull
    # def __init__(self, user_id: uuid.UUID):
    #     self.user = User.objects.get(pk=user_id)
    def _get_user(self, user_id) -> User:
        return User.objects.get(pk=user_id)
    
    def set_role(self, user_id: uuid.UUID, role: str) -> None:
        user = self._get_user(user_id)
        user.set_role(role)

    def revoke_role(self, user_id: uuid.UUID) -> None:
        user = self._get_user(user_id)
        user.revoke_role()

    def get_role(self, user_id: uuid.UUID) -> str:
        user = self._get_user(user_id)
        return user.get_role