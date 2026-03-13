from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, SupplierViewSet, CustomerViewSet, GoodsViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('suppliers', SupplierViewSet, basename='suppliers')
router.register('customers', CustomerViewSet, basename='customers')
router.register('goods', GoodsViewSet, basename='goods')

urlpatterns = router.urls
