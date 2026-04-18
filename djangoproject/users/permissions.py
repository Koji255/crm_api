from rest_framework.permissions import BasePermission
from .models import User
from backend.structures import GroupEnum


class _HasRole(BasePermission):
    required_role = None

    def has_permission(self, request, view):
        user: User = request.user
        return user.is_authenticated and user.has_role(self.required_role)

class isDirector(_HasRole):
    required_role = GroupEnum.DIRECTOR.value
    
class isManager(_HasRole):
    required_role = GroupEnum.MANAGER.value
    
class isAnalyst(_HasRole):
    required_role = GroupEnum.ANALYST.value