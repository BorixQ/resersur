from django.db import models
from django.conf import settings
from vehicles.models import Vehicle

class WorkOrder(models.Model):
    ESTADOS_OT = [
        ('cita', 'Cita Programada'),
        ('diagnostico', 'Diagnóstico'),
        ('cotizacion', 'Cotización'),
        ('aprobada', 'Aprobada'),
        ('taller', 'En Taller'),
        ('qc', 'Control Calidad'),
        ('listo', 'Listo para Entregar'),
        ('entregado', 'Entregado'),
    ]

    numero = models.CharField(max_length=20, unique=True)
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ordenes_cliente')
    asesor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes_asesor')
    vehiculo = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS_OT, default='cita')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"OT-{self.numero} - {self.vehiculo.placa}"
