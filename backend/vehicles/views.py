# vehicles/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import Vehicle
from .serializers import VehicleSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'cliente':
            return Vehicle.objects.filter(cliente=user)
        return Vehicle.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        if user.rol == 'cliente':
            serializer.save(cliente=user)
        elif user.rol in ['asesor', 'supervisor', 'admin']:
            serializer.save()
        else:
            raise PermissionDenied("No tienes permiso para crear vehículos.")

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if user.rol == 'cliente' and instance.cliente != user:
            raise PermissionDenied("No puedes editar vehículos de otros usuarios.")

        if user.rol not in ['cliente', 'asesor', 'supervisor', 'admin']:
            raise PermissionDenied("No tienes permiso para editar vehículos.")

        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if user.rol not in ['asesor', 'supervisor', 'admin']:
            raise PermissionDenied("No tienes permiso para eliminar vehículos.")
        return super().destroy(request, *args, **kwargs)
