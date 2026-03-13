from django.db import transaction
from .models import Stock, StockBatch


class StockService:
    @staticmethod
    @transaction.atomic
    def increase(warehouse_id, goods_id, qty, batch_no='', prod_date=None, exp_date=None):
        stock, _ = Stock.objects.select_for_update().get_or_create(
            warehouse_id=warehouse_id,
            goods_id=goods_id,
            defaults={'quantity': 0, 'locked_qty': 0},
        )
        stock.quantity += qty
        stock.save()

        batch, _ = StockBatch.objects.select_for_update().get_or_create(
            warehouse_id=warehouse_id,
            goods_id=goods_id,
            batch_no=batch_no or '',
            defaults={
                'quantity': 0,
                'locked_qty': 0,
                'prod_date': prod_date,
                'exp_date': exp_date,
            },
        )
        batch.quantity += qty
        if prod_date:
            batch.prod_date = prod_date
        if exp_date:
            batch.exp_date = exp_date
        batch.save()

    @staticmethod
    @transaction.atomic
    def freeze(warehouse_id, goods_id, qty, batch_no=''):
        stock = Stock.objects.select_for_update().get(
            warehouse_id=warehouse_id,
            goods_id=goods_id,
        )
        if stock.quantity - stock.locked_qty < qty:
            raise Exception('可用库存不足')
        stock.locked_qty += qty
        stock.save()

        batch = StockBatch.objects.select_for_update().get(
            warehouse_id=warehouse_id,
            goods_id=goods_id,
            batch_no=batch_no or '',
        )
        if batch.quantity - batch.locked_qty < qty:
            raise Exception('批次可用库存不足')
        batch.locked_qty += qty
        batch.save()

    @staticmethod
    @transaction.atomic
    def deduct(warehouse_id, goods_id, qty, batch_no=''):
        stock = Stock.objects.select_for_update().get(
            warehouse_id=warehouse_id,
            goods_id=goods_id,
        )
        if stock.quantity < qty:
            raise Exception('库存不足')
        if stock.locked_qty < qty:
            raise Exception('冻结量不足')
        stock.quantity -= qty
        stock.locked_qty -= qty
        stock.save()

        batch = StockBatch.objects.select_for_update().get(
            warehouse_id=warehouse_id,
            goods_id=goods_id,
            batch_no=batch_no or '',
        )
        if batch.quantity < qty:
            raise Exception('批次库存不足')
        if batch.locked_qty < qty:
            raise Exception('批次冻结量不足')
        batch.quantity -= qty
        batch.locked_qty -= qty
        batch.save()

    @staticmethod
    @transaction.atomic
    def release(warehouse_id, goods_id, qty, batch_no=''):
        stock = Stock.objects.select_for_update().get(
            warehouse_id=warehouse_id,
            goods_id=goods_id,
        )
        if stock.locked_qty < qty:
            raise Exception('冻结量不足，无法释放')
        stock.locked_qty -= qty
        stock.save()

        batch = StockBatch.objects.select_for_update().get(
            warehouse_id=warehouse_id,
            goods_id=goods_id,
            batch_no=batch_no or '',
        )
        if batch.locked_qty < qty:
            raise Exception('批次冻结量不足，无法释放')
        batch.locked_qty -= qty
        batch.save()
