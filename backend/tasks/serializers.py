from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['fecha_asignacion', 'fecha_completado']

    def update(self, instance, validated_data):
        # Si la tarea se marca como completada, se guarda timestamp
        if validated_data.get('estado') == 'completado' and not instance.fecha_completado:
            from django.utils import timezone
            instance.fecha_completado = timezone.now()
        return super().update(instance, validated_data)
