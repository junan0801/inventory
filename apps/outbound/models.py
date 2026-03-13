from django.db import models
from apps.goods.models import Customer, Goods
from apps.users.models import SysUser
from apps.warehouse.models import Warehouse


class OutOrder(models.Model):
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('pending', '待审核'),
        ('frozen', '已冻结'),
        ('done', '已出库'),
        ('cancelled', '作废'),
    )

    TYPE_CHOICES = (
        ('sale', '销售出库'),
        ('use', '领用出库'),
        ('scrap', '报废出库'),
    )

    order_no = models.CharField(max_length=64, unique=True)
    out_type = models.CharField(max_length=32, choices=TYPE_CHOICES)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='draft')
    create_user = models.ForeignKey(SysUser, on_delete=models.SET_NULL, null=True, related_name='created_out_orders')
    audit_user = models.ForeignKey(SysUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='audited_out_orders')
    create_time = models.DateTimeField(auto_now_add=True)
    audit_time = models.DateTimeField(null=True, blank=True)
    remark = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'out_order'


class OutDetail(models.Model):
    order = models.ForeignKey(OutOrder, on_delete=models.CASCADE, related_name='details')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    batch_no = models.CharField(max_length=64, blank=True, null=True)
    req_qty = models.IntegerField()
    frozen_qty = models.IntegerField(default=0)
    actual_qty = models.IntegerField(default=0)

    class Meta:
        db_table = 'out_detail'
