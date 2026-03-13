from rest_framework import serializers
from .models import InOrder, InDetail


class InDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InDetail
        fields = '__all__'


class InOrderSerializer(serializers.ModelSerializer):
    details = InDetailSerializer(many=True)

    class Meta:
        model = InOrder
        fields = '__all__'
        read_only_fields = ('create_user', 'audit_user', 'audit_time', 'create_time')

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        order = InOrder.objects.create(**validated_data)
        for item in details_data:
            InDetail.objects.create(order=order, **item)
        return order

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()

        if details_data is not None and instance.status == 'draft':
            instance.details.all().delete()
            for item in details_data:
                InDetail.objects.create(order=instance, **item)
        return instance
