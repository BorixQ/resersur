# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin URL
    path('api/accounts/', include('accounts.urls')),  # Incluye las rutas de la app accounts
    path('api/vehicles/', include('vehicles.urls')),
    path('api/orders/', include('orders.urls')),

]
