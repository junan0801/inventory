from django.db import transaction
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from .models import InOrder
from .serializers import InOrderSerializer
from apps.inventory.services import StockService


class InOrderViewSet(ModelViewSet):
    queryset = InOrder.objects.all().order_by('-id')
    serializer_class = InOrderSerializer

    def perform_create(self, serializer):
        serializer.save(create_user=self.request.user)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        order = self.get_object()
        if order.status != 'draft':
            return Response({'detail': '只有草稿单可以提交'}, status=status.HTTP_400_BAD_REQUEST)
        order.status = 'pending'
        order.save()
        return Response({'detail': '提交成功'})

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def approve(self, request, pk=None):
        order = self.get_object()
        if order.status != 'pending':
            return Response({'detail': '只有待审核单可以审核'}, status=status.HTTP_400_BAD_REQUEST)

        for detail in order.details.all():
            StockService.increase(
                warehouse_id=detail.warehouse_id,
                goods_id=detail.goods_id,
                qty=detail.qty,
                batch_no=detail.batch_no or '',
                prod_date=detail.prod_date,
                exp_date=detail.exp_date,
            )

        order.status = 'approved'
        order.audit_user = request.user
        order.audit_time = timezone.now()
        order.save()

        return Response({'detail': '审核成功，库存已增加'})
