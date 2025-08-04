from rest_framework import serializers
from orders.models.photos import OTPhoto

class OTPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPhoto
        fields = '__all__'
        read_only_fields = ['fecha_subida', 'usuario']
