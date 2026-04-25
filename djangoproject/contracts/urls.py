from rest_framework import routers
from .views import ContractListRetrieveViewSet

router = routers.SimpleRouter()
router.register(r'contracts', ContractListRetrieveViewSet, basename='contracts')

urlpatterns =[
]
urlpatterns+=router.urls