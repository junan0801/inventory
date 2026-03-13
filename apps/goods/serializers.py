from rest_framework import serializers
from .models import Category, Supplier, Customer, Goods


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.cat_name', read_only=True)

    class Meta:
        model = Goods
        fields = '__all__'
