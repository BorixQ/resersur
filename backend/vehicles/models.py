#vehicles/models.py

from django.db import models
from django.conf import settings

class Vehicle(models.Model):
    TIPO_VEHICULO = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('minivan', 'Minivan'),
        ('camioneta', 'Camioneta'),
        ('furgon','Furgon'),
        ('hatchback','Hatchback')
    ]

    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vehiculos')
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.PositiveIntegerField()
    placa = models.CharField(max_length=15, unique=True)
    color = models.CharField(max_length=30)
    tipo = models.CharField(max_length=20, choices=TIPO_VEHICULO)

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo}"
