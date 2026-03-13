from django.db import models
from apps.goods.models import Goods
from apps.warehouse.models import Warehouse


class Stock(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    locked_qty = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stock'
        unique_together = ('warehouse', 'goods')

    @property
    def available_qty(self):
        return self.quantity - self.locked_qty


class StockBatch(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    batch_no = models.CharField(max_length=64, default='', blank=True)
    quantity = models.IntegerField(default=0)
    locked_qty = models.IntegerField(default=0)
    prod_date = models.DateField(null=True, blank=True)
    exp_date = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stock_batch'
        unique_together = ('warehouse', 'goods', 'batch_no')

    @property
    def available_qty(self):
        return self.quantity - self.locked_qty
