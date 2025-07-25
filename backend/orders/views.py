from rest_framework import viewsets, permissions
from .models import WorkOrder
from .serializers import WorkOrderSerializer

class WorkOrderViewSet(viewsets.ModelViewSet):
    serializer_class = WorkOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'cliente':
            return WorkOrder.objects.filter(cliente=user)
        return WorkOrder.objects.all()
