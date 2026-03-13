from django.db import models


class Warehouse(models.Model):
    name = models.CharField(max_length=128, verbose_name='仓库名称')
    address = models.CharField(max_length=255, blank=True, null=True)
    manager = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        db_table = 'warehouse'
        verbose_name = '仓库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
