from django.db import models


class Category(models.Model):
    cat_name = models.CharField(max_length=128, verbose_name='分类名称')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')

    class Meta:
        db_table = 'category'
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.cat_name


class Supplier(models.Model):
    name = models.CharField(max_length=255, verbose_name='供应商名称')
    contact = models.CharField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'supplier'
        verbose_name = '供应商'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=255, verbose_name='客户名称')
    contact = models.CharField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        db_table = 'customer'
        verbose_name = '客户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(models.Model):
    sn = models.CharField(max_length=64, unique=True, verbose_name='编码')
    name = models.CharField(max_length=255, verbose_name='名称')
    spec = models.CharField(max_length=255, blank=True, null=True, verbose_name='规格')
    unit = models.CharField(max_length=32, verbose_name='单位')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    safety_stock = models.IntegerField(default=0, verbose_name='安全库存')

    class Meta:
        db_table = 'goods'
        verbose_name = '物料'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.sn}-{self.name}'
