# /orders/views/workorder.py

from rest_framework import generics, permissions
from orders.models.workorder import WorkOrder
from orders.serializers.workorder import WorkOrderSerializer
from rest_framework.exceptions import PermissionDenied

class WorkOrderListView(generics.ListCreateAPIView):
    serializer_class = WorkOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'cliente':
            return WorkOrder.objects.filter(cliente=user)
        return WorkOrder.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        estado = self.request.data.get('estado')

        if user.rol == 'cliente':
            if estado != 'cita':
                raise PermissionDenied("Clientes solo pueden crear OTs con estado 'cita'.")
            serializer.save(cliente=user)
        elif user.rol in ['asesor', 'supervisor', 'admin']:
            cliente_id = self.request.data.get('cliente')
            from accounts.models import CustomUser
            cliente_obj = CustomUser.objects.filter(id=cliente_id, rol='cliente').first()

            if not cliente_obj:
                raise PermissionDenied("El cliente debe ser un usuario con rol 'cliente'.")

            serializer.save()
        else:
            raise PermissionDenied("No tienes permiso para crear OTs.")

class WorkOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if user.rol == 'cliente' and obj.cliente != user:
            raise PermissionDenied("No puedes acceder a esta OT.")
        return obj

    def perform_update(self, serializer):
        user = self.request.user
        if user.rol not in ['asesor', 'supervisor', 'admin']:
            raise PermissionDenied("No tienes permiso para modificar esta OT.")
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        if user.rol not in ['asesor', 'supervisor', 'admin']:
            raise PermissionDenied("No tienes permiso para eliminar esta OT.")
        instance.delete()
