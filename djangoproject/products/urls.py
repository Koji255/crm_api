from rest_framework import routers
from django.urls import path
from .views import CourseViewSet

router = routers.SimpleRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
]
urlpatterns += router.urls