from rest_framework import serializers
from .models import Stock, StockBatch


class StockSerializer(serializers.ModelSerializer):
    goods_name = serializers.CharField(source='goods.name', read_only=True)
    goods_sn = serializers.CharField(source='goods.sn', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    available_qty = serializers.IntegerField(read_only=True)

    class Meta:
        model = Stock
        fields = '__all__'


class StockBatchSerializer(serializers.ModelSerializer):
    goods_name = serializers.CharField(source='goods.name', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    available_qty = serializers.IntegerField(read_only=True)

    class Meta:
        model = StockBatch
        fields = '__all__'
