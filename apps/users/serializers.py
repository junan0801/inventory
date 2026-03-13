from rest_framework import serializers
from .models import SysUser


class SysUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysUser
        fields = ['id', 'username', 'real_name', 'phone', 'is_active', 'is_staff', 'is_superuser']
