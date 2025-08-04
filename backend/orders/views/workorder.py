# /orders/views/workorder.py

from rest_framework import generics, permissions
from orders.models.workorder import WorkOrder
from orders.serializers.workorder import WorkOrderSerializer
from rest_framework.exceptions import PermissionDenied

class WorkOrderListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'cliente':
            return WorkOrder.objects.filter(cliente=user)
        return WorkOrder.objects.all()

    def perform_create(self, serializer):
        user = self.request.user

        if user.rol not in ['asesor', 'supervisor', 'admin']:
            raise PermissionDenied("Solo el personal autorizado puede crear órdenes de trabajo.")

        serializer.save()

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
