from django.contrib.auth.models import AbstractUser
from django.db import models

# Definir los roles de usuario como un choice field
ROLES = (
    ('cliente', 'Cliente'),
    ('asesor', 'Asesor'),
    ('supervisor', 'Supervisor'),
    ('tecnico', 'Técnico'),
    ('codificador', 'Codificador'),
    ('admin', 'Administrador'),
)

class CustomUser(AbstractUser):
    # Campos personalizados
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='cliente')
    
    # Campos específicos por rol
    dni_ruc = models.CharField(max_length=20, blank=True, null=True)  # Para clientes
    fecha_nacimiento = models.DateField(blank=True, null=True)  # Para clientes
    codigo_empleado = models.CharField(max_length=20, blank=True, null=True)  # Para asesor, supervisor, técnico, codificador
    area = models.CharField(max_length=100, blank=True, null=True)  # Para técnicos

    # Hacer el email único
    email = models.EmailField(unique=True)

    # Cambiar el campo username por email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Ya no es necesario 'username'

    def __str__(self):
        return self.email
