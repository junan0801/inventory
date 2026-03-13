from django.db import transaction
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from .models import OutOrder
from .serializers import OutOrderSerializer
from apps.inventory.services import StockService


class OutOrderViewSet(ModelViewSet):
    queryset = OutOrder.objects.all().order_by('-id')
    serializer_class = OutOrderSerializer

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
    def freeze(self, request, pk=None):
        order = self.get_object()
        if order.status != 'pending':
            return Response({'detail': '只有待审核单可以冻结'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            for detail in order.details.all():
                StockService.freeze(
                    warehouse_id=detail.warehouse_id,
                    goods_id=detail.goods_id,
                    qty=detail.req_qty,
                    batch_no=detail.batch_no or '',
                )
                detail.frozen_qty = detail.req_qty
                detail.save()

            order.status = 'frozen'
            order.audit_user = request.user
            order.audit_time = timezone.now()
            order.save()
            return Response({'detail': '冻结成功'})
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def confirm(self, request, pk=None):
        order = self.get_object()
        if order.status != 'frozen':
            return Response({'detail': '只有已冻结单可以确认出库'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            for detail in order.details.all():
                actual_qty = detail.actual_qty if detail.actual_qty > 0 else detail.frozen_qty
                StockService.deduct(
                    warehouse_id=detail.warehouse_id,
                    goods_id=detail.goods_id,
                    qty=actual_qty,
                    batch_no=detail.batch_no or '',
                )
                detail.actual_qty = actual_qty
                detail.save()

            order.status = 'done'
            order.save()
            return Response({'detail': '出库成功'})
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status == 'done':
            return Response({'detail': '已出库单不能作废'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if order.status == 'frozen':
                for detail in order.details.all():
                    if detail.frozen_qty > 0:
                        StockService.release(
                            warehouse_id=detail.warehouse_id,
                            goods_id=detail.goods_id,
                            qty=detail.frozen_qty,
                            batch_no=detail.batch_no or '',
                        )
                        detail.frozen_qty = 0
                        detail.save()

            order.status = 'cancelled'
            order.save()
            return Response({'detail': '作废成功'})
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
