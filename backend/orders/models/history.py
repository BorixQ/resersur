from django.db import models
from django.conf import settings
from .workorder import WorkOrder

class OTStatusHistory(models.Model):
    ot = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='historial')
    estado = models.CharField(max_length=20)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.ot.numero} - {self.estado} ({self.timestamp})"
