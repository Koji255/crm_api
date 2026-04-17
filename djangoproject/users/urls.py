from django.urls import path
from .views import RoleAPIView

urlpatterns = [
    path('<uuid:user_id>/role/', view=RoleAPIView.as_view(), name='role_set_revoke'),
]