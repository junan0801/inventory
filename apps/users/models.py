from django.db import models
from django.contrib.auth.models import AbstractUser


class SysUser(AbstractUser):
    real_name = models.CharField(max_length=64, blank=True, null=True, verbose_name='姓名')
    phone = models.CharField(max_length=32, blank=True, null=True, verbose_name='电话')

    class Meta:
        db_table = 'sys_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
