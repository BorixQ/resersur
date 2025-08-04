# /orders/models/workorder.py
from django.db import models
from django.conf import settings
from vehicles.models import Vehicle

TIPO_CLIENTE = [
    ('particular', 'Particular'),
    ('asegurado', 'Asegurado'),
]

ESTADOS_OT = [
    ('recepcion', 'Recepción'),
    ('diagnostico', 'Diagnóstico'),
    ('cotizacion', 'Cotización'),
    ('aprobada', 'Aprobada'),
    ('taller', 'En Taller'),
    ('qc', 'Control Calidad'),
    ('listo', 'Listo para Entregar'),
    ('entregado', 'Entregado'),
    ('cerrado', 'Cerrado'),
]

class WorkOrder(models.Model):
    numero = models.CharField(max_length=20, unique=True)
    
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ordenes_cliente',
        limit_choices_to={'rol': 'cliente'}
    )

    asesor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ordenes_asesor',
        limit_choices_to={'rol': 'asesor'}
    )

    vehiculo = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    tipo_cliente = models.CharField(max_length=20, choices=TIPO_CLIENTE, default='asegurado')
    internamiento = models.BooleanField(default=False)
    estado = models.CharField(max_length=20, choices=ESTADOS_OT, default='recepcion')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"OT-{self.numero} - {self.vehiculo.placa}"

    def save(self, *args, **kwargs):
        if self.pk:
            from orders.models.history import OTStatusHistory
            previous = WorkOrder.objects.get(pk=self.pk)
            if previous.estado != self.estado:
                OTStatusHistory.objects.create(
                    ot=self,
                    estado=self.estado,
                    usuario=self.asesor or self.cliente
                )
        super().save(*args, **kwargs)
