from rest_framework import routers
from django.urls import path
from .views import DealViewSet

router = routers.SimpleRouter()
router.register(r'deals', DealViewSet, basename='deals')

urlpatterns = [
]
urlpatterns += router.urls