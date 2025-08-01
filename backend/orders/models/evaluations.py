from django.db import models
from django.conf import settings
from .workorder import WorkOrder

class DamageEvaluation(models.Model):
    ot = models.OneToOneField(WorkOrder, on_delete=models.CASCADE, related_name='evaluacion')
    tecnico = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, limit_choices_to={'rol': 'tecnico'})
    descripcion_general = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evaluación OT-{self.ot.numero}"
