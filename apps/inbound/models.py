from django.db import models
from apps.goods.models import Supplier, Goods
from apps.users.models import SysUser
from apps.warehouse.models import Warehouse


class InOrder(models.Model):
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('pending', '待审核'),
        ('approved', '已审核'),
        ('cancelled', '作废'),
    )

    TYPE_CHOICES = (
        ('purchase', '采购入库'),
        ('profit', '盘盈入库'),
    )

    order_no = models.CharField(max_length=64, unique=True)
    in_type = models.CharField(max_length=32, choices=TYPE_CHOICES)
    supplier = models.ForeignKey(Supplier, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='draft')
    create_user = models.ForeignKey(SysUser, on_delete=models.SET_NULL, null=True, related_name='created_in_orders')
    audit_user = models.ForeignKey(SysUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='audited_in_orders')
    create_time = models.DateTimeField(auto_now_add=True)
    audit_time = models.DateTimeField(null=True, blank=True)
    remark = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'in_order'


class InDetail(models.Model):
    order = models.ForeignKey(InOrder, on_delete=models.CASCADE, related_name='details')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    batch_no = models.CharField(max_length=64, blank=True, null=True)
    qty = models.IntegerField()
    price = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    prod_date = models.DateField(null=True, blank=True)
    exp_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'in_detail'
