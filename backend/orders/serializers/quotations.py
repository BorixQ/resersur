from rest_framework import serializers
from orders.models.quotations import Quotation

class QuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = '__all__'
        read_only_fields = ['version', 'fecha_creacion']

    def create(self, validated_data):
        ot = validated_data['ot']
        last_version = Quotation.objects.filter(ot=ot).count()
        validated_data['version'] = last_version + 1

        # Desactivar las versiones anteriores
        Quotation.objects.filter(ot=ot).update(activa=False)
        validated_data['activa'] = True

        return super().create(validated_data)
