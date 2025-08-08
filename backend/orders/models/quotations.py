from django.db import models
from django.conf import settings
from orders.models.workorder import WorkOrder

class Quotation(models.Model):
    ot = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='cotizaciones')
    version = models.IntegerField()
    descripcion = models.TextField(default='Sin descripción', blank=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    es_aprobada = models.BooleanField(default=False)
    archivo_adjunto = models.FileField(upload_to='cotizaciones/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('ot', 'version')
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Cotización v{self.version} para OT-{self.ot.numero}"
