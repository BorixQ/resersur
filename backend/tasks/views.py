from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer
from orders.permissions import IsTecnico, IsSupervisor

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'tecnico':
            return Task.objects.filter(tecnico=user)
        if user.rol == 'supervisor':
            return Task.objects.all()
        return Task.objects.none()

    def perform_create(self, serializer):
        return serializer.save()
