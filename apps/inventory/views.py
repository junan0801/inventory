from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Stock, StockBatch
from .serializers import StockSerializer, StockBatchSerializer


class StockViewSet(ReadOnlyModelViewSet):
    queryset = Stock.objects.all().order_by('-id')
    serializer_class = StockSerializer
    filterset_fields = ['warehouse', 'goods']


class StockBatchViewSet(ReadOnlyModelViewSet):
    queryset = StockBatch.objects.all().order_by('-id')
    serializer_class = StockBatchSerializer
    filterset_fields = ['warehouse', 'goods', 'batch_no']
