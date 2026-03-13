from rest_framework.routers import DefaultRouter
from .views import InOrderViewSet

router = DefaultRouter()
router.register('in-orders', InOrderViewSet, basename='in-orders')

urlpatterns = router.urls
