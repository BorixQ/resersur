# /orders/serializers/workorder.py

from rest_framework import serializers
from orders.models.workorder import WorkOrder
from accounts.models import CustomUser

class WorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields = '__all__'
        read_only_fields = ['fecha_creacion', 'numero']

    def validate(self, data):
        cliente = data.get('cliente')
        asesor = data.get('asesor')

        if cliente and cliente.rol != 'cliente':
            raise serializers.ValidationError("El usuario asignado como cliente no tiene rol 'cliente'.")

        if asesor and asesor.rol != 'asesor':
            raise serializers.ValidationError("El asesor debe tener rol 'asesor'.")

        return data

    def create(self, validated_data):
        from datetime import datetime
        now = datetime.now()
        prefix = f"OT-{now.strftime('%Y%m%d')}"
        count = WorkOrder.objects.filter(numero__startswith=prefix).count() + 1
        validated_data['numero'] = f"{prefix}-{count:03}"
        return super().create(validated_data)
