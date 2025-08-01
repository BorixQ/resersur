from rest_framework import serializers
from orders.models.photos import OTPhoto

class OTPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPhoto
        fields = '__all__'
        read_only_fields = ['tecnico', 'fecha_subida']

    def create(self, validated_data):
        validated_data['tecnico'] = self.context['request'].user
        return super().create(validated_data)
