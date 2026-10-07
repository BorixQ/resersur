# RESERSUR — backend de gestión de taller

API en Django REST Framework para gestionar usuarios, vehículos, órdenes de trabajo y tareas de técnicos.

## Funcionalidades presentes en el código

- Usuarios, roles y autenticación JWT.
- Registro de vehículos asociados a clientes.
- Órdenes de trabajo con evaluaciones, fotografías, cotizaciones e historial de estados.
- Asignación de tareas y seguimiento de su estado.

## Tecnologías

Python, Django, Django REST Framework, Simple JWT y MySQL. El repositorio incluye configuración para Docker Compose.

## Estructura

| Ruta | Función |
| --- | --- |
| `backend/accounts/` | Usuarios, roles y autenticación. |
| `backend/vehicles/` | Vehículos de clientes. |
| `backend/orders/` | Órdenes, evaluaciones, fotografías, cotizaciones e historial. |
| `backend/tasks/` | Tareas asignadas a técnicos. |
| `backend/backend/` | Configuración y rutas del proyecto Django. |
| `backend/requirements.txt` | Dependencias del backend. |
| `docker-compose.yml` | Servicios del backend y MySQL. |

## Preparar el entorno

```bash
git clone https://github.com/BorixQ/resersur.git
cd resersur
```

Antes de iniciar los servicios, revisa estos puntos del estado actual:

- Compose referencia `backend/Dockerfile`, mientras que el archivo versionado se llama `backend/dockerfile`. Deben coincidir en sistemas que distinguen mayúsculas.
- La imagen usa Python 3.12 y las dependencias fijan Django 3.2.9; la compatibilidad del conjunto debe revisarse.
- La configuración de MySQL se define en `backend/backend/settings.py`. Los valores de conexión deben coincidir con el servicio `db`.
- `DEBUG`, `ALLOWED_HOSTS` y los valores de configuración requieren adaptación al entorno.

Una vez revisada la configuración:

```bash
docker compose up --build
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
```

El servicio del backend se configura en http://localhost:8000.

## Estado

La configuración versionada corresponde a desarrollo. Este README describe el código disponible; no certifica un despliegue de producción ni una ejecución verificada.

El repositorio contiene archivos `tests.py` en sus aplicaciones. Su presencia no demuestra cobertura funcional; conviene añadir pruebas de permisos, órdenes de trabajo y asignación de tareas antes de usarlo como referencia de calidad.
