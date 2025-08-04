from django.db import models
from django.conf import settings
from orders.models.workorder import WorkOrder

class DamageEvaluation(models.Model):
    ot = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='evaluaciones')
    tecnico = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'rol__in': ['tecnico', 'asesor', 'supervisor', 'admin']}
    )
    descripcion_general = models.TextField()
    observaciones = models.TextField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Evaluación OT-{self.ot.numero} por {self.tecnico}"
