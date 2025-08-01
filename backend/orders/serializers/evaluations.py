from rest_framework import serializers
from orders.models.evaluations import DamageEvaluation

class DamageEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DamageEvaluation
        fields = '__all__'
        read_only_fields = ['tecnico', 'fecha']

    def create(self, validated_data):
        validated_data['tecnico'] = self.context['request'].user
        return super().create(validated_data)
