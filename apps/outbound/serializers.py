from rest_framework import serializers
from .models import OutOrder, OutDetail


class OutDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutDetail
        fields = '__all__'


class OutOrderSerializer(serializers.ModelSerializer):
    details = OutDetailSerializer(many=True)

    class Meta:
        model = OutOrder
        fields = '__all__'
        read_only_fields = ('create_user', 'audit_user', 'audit_time', 'create_time')

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        order = OutOrder.objects.create(**validated_data)
        for item in details_data:
            OutDetail.objects.create(order=order, **item)
        return order

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()

        if details_data is not None and instance.status == 'draft':
            instance.details.all().delete()
            for item in details_data:
                OutDetail.objects.create(order=instance, **item)
        return instance
