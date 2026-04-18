from rest_framework.permissions import BasePermission
from typing import List
from .models import User
from backend.structures import GroupEnum

class _HasRole(BasePermission):
    required_roles: List[str] = []

    def has_permission(self, request, view):
        user: User = request.user
        # if len(self.required_roles) == 1: #If there are only one required role & no need 
        if not user.is_authenticated:
            return False
        for role in self.required_roles:
            if user.has_role(role): #if user has at least 1 required role return true
                return True
        return False
        

class isDirector(_HasRole):
    required_roles = [GroupEnum.DIRECTOR.value]
    
class isManager(_HasRole):
    required_roles = [GroupEnum.MANAGER.value]
    
class isAnalyst(_HasRole):
    required_roles = [GroupEnum.ANALYST.value]

class isManagerOrDirector(_HasRole):
    required_roles = [GroupEnum.MANAGER.value, GroupEnum.DIRECTOR.value]