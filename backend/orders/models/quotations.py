from django.db import models
from .workorder import WorkOrder

class Quotation(models.Model):
    ot = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='cotizaciones')
    version = models.PositiveIntegerField()
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    pdf = models.FileField(upload_to='cotizaciones/')
    activa = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('ot', 'version')

    def __str__(self):
        return f"Cotización {self.ot.numero} v{self.version}"
