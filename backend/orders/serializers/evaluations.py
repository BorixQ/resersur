from rest_framework import serializers
from orders.models.evaluations import DamageEvaluation

class DamageEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DamageEvaluation
        fields = '__all__'
        read_only_fields = ['creado_en', 'actualizado_en']
