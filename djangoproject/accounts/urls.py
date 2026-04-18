from .views import AccountModelViewSet, ContactModelViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'accounts', AccountModelViewSet)
router.register(r'contacts', ContactModelViewSet)

urlpatterns = [

]
urlpatterns += router.urls