from django.db import models
from django.conf import settings
from .workorder import WorkOrder

TIPO_FOTO = [
    ('inicio', 'Inicial'),
    ('avance', 'Avance'),
    ('calidad', 'Control de Calidad'),
]

class OTPhoto(models.Model):
    ot = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='fotos')
    tipo = models.CharField(max_length=20, choices=TIPO_FOTO)
    imagen = models.ImageField(upload_to='fotos_ot/')
    tecnico = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ot.numero} - {self.tipo}"
