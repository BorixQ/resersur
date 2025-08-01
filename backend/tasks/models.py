from django.db import models
from django.conf import settings
from orders.models import WorkOrder

ESTADO_TAREA = [
    ('pendiente', 'Pendiente'),
    ('en_proceso', 'En proceso'),
    ('completado', 'Completado'),
]

class Task(models.Model):
    ot = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='tareas')
    tecnico = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'rol': 'tecnico'}
    )
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_TAREA, default='pendiente')
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    fecha_completado = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Tarea OT-{self.ot.numero} - {self.tecnico}"
