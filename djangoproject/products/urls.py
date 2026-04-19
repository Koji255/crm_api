from rest_framework import routers
from django.urls import path
from .views import CourseViewSet, ProductItemModelViewSet

router = routers.SimpleRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'product-items', ProductItemModelViewSet, basename='product_items')


urlpatterns = [
]
urlpatterns += router.urls