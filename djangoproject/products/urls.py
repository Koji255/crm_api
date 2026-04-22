from rest_framework import routers
from django.urls import path
from .views import CourseViewSet#, ProductItemViewSet

router = routers.SimpleRouter()
router.register(r'courses', CourseViewSet, basename='courses')
# router.register(r'product-items', ProductItemViewSet, basename='product_items')


urlpatterns = [
]
urlpatterns += router.urls