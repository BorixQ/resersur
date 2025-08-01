from rest_framework import serializers
from orders.models.history import OTStatusHistory

class OTStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OTStatusHistory
        fields = '__all__'
        read_only_fields = ['timestamp']
