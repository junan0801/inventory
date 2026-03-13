from rest_framework.routers import DefaultRouter
from .views import OutOrderViewSet

router = DefaultRouter()
router.register('out-orders', OutOrderViewSet, basename='out-orders')

urlpatterns = router.urls
