from django.db import models
from django.conf import settings
from orders.models.workorder import WorkOrder

class OTStatusHistory(models.Model):
    ot = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='historial_estado')
    estado = models.CharField(max_length=20)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    comentario = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.ot.numero} → {self.estado} ({self.fecha_cambio.date()})"
