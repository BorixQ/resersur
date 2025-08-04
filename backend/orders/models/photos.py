from django.db import models
from django.conf import settings
from orders.models.workorder import WorkOrder

TIPO_FOTO = [
    ('inicio', 'Inicio'),
    ('avance', 'Avance'),
    ('qc', 'Control de Calidad'),
    ('final', 'Final'),
    ('otro', 'Otro'),
]

class OTPhoto(models.Model):
    ot = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='fotos')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    tipo = models.CharField(max_length=20, choices=TIPO_FOTO)
    imagen = models.ImageField(upload_to='fotos_ots/')
    descripcion = models.TextField(blank=True, null=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo.upper()} - OT-{self.ot.numero}"
