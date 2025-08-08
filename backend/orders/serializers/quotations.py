from rest_framework import serializers
from orders.models.quotations import Quotation

class QuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = '__all__'
        read_only_fields = ['version', 'creado_por', 'fecha_creacion']

    def create(self, validated_data):
        ot = validated_data['ot']
        last_version = Quotation.objects.filter(ot=ot).order_by('-version').first()
        validated_data['version'] = (last_version.version + 1) if last_version else 1
        validated_data['creado_por'] = self.context['request'].user
        return super().create(validated_data)
