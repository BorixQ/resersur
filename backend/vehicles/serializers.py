# vehicles/serializers.py
from rest_framework import serializers
from .models import Vehicle

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'
        read_only_fields = ['cliente']

    def create(self, validated_data):
        validated_data['cliente'] = self.context['request'].user
        return super().create(validated_data)
