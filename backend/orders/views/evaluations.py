from rest_framework import generics, permissions
from orders.models.evaluations import DamageEvaluation
from orders.serializers.evaluations import DamageEvaluationSerializer
from rest_framework.exceptions import PermissionDenied

class DamageEvaluationListCreateView(generics.ListCreateAPIView):
    serializer_class = DamageEvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'tecnico':
            return DamageEvaluation.objects.filter(tecnico=user)
        return DamageEvaluation.objects.all()

    def perform_create(self, serializer):
        user = self.request.user

        if user.rol not in ['tecnico', 'asesor', 'supervisor', 'admin']:
            raise PermissionDenied("No tienes permiso para registrar evaluaciones.")

        # Si el usuario es técnico, asignarse automáticamente
        if user.rol == 'tecnico':
            serializer.save(tecnico=user)
        else:
            # Roles internos deben proporcionar un técnico explícitamente
            tecnico_id = self.request.data.get('tecnico')
            if not tecnico_id:
                raise PermissionDenied("Debes especificar el ID de un técnico.")

            from accounts.models import CustomUser
            tecnico = CustomUser.objects.filter(id=tecnico_id, rol='tecnico').first()
            if not tecnico:
                raise PermissionDenied("El ID proporcionado no pertenece a un técnico válido.")

            serializer.save(tecnico=tecnico)


class DamageEvaluationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DamageEvaluation.objects.all()
    serializer_class = DamageEvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if user.rol == 'cliente':
            raise PermissionDenied("No puedes acceder a evaluaciones.")
        if user.rol == 'tecnico' and obj.tecnico != user:
            raise PermissionDenied("Solo puedes ver tus evaluaciones.")
        return obj
