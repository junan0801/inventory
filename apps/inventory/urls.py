from rest_framework.routers import DefaultRouter
from .views import StockViewSet, StockBatchViewSet

router = DefaultRouter()
router.register('stocks', StockViewSet, basename='stocks')
router.register('stock-batches', StockBatchViewSet, basename='stock-batches')

urlpatterns = router.urls
