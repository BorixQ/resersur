# orders/serializers.py
from rest_framework import serializers
from .models import WorkOrder

class WorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields = '__all__'
        read_only_fields = ['cliente', 'numero', 'fecha_creacion']

    def create(self, validated_data):
        # Autogenerar número de OT
        validated_data['cliente'] = self.context['request'].user
        validated_data['numero'] = self.generar_num_ot()
        return super().create(validated_data)

    def generar_num_ot(self):
        from datetime import datetime
        now = datetime.now()
        prefix = f"OT-{now.strftime('%Y%m%d')}"
        count = WorkOrder.objects.filter(numero__startswith=prefix).count() + 1
        return f"{prefix}-{count:03}"
