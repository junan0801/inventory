from rest_framework.viewsets import ModelViewSet
from .models import Warehouse
from .serializers import WarehouseSerializer


class WarehouseViewSet(ModelViewSet):
    queryset = Warehouse.objects.all().order_by('-id')
    serializer_class = WarehouseSerializer
