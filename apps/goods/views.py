from rest_framework.viewsets import ModelViewSet
from .models import Category, Supplier, Customer, Goods
from .serializers import CategorySerializer, SupplierSerializer, CustomerSerializer, GoodsSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer


class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all().order_by('-id')
    serializer_class = SupplierSerializer


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all().order_by('-id')
    serializer_class = CustomerSerializer


class GoodsViewSet(ModelViewSet):
    queryset = Goods.objects.all().order_by('-id')
    serializer_class = GoodsSerializer
    filterset_fields = ['category']
