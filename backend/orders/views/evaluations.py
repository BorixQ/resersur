from rest_framework import generics, permissions
from orders.models.evaluations import DamageEvaluation
from orders.serializers.evaluations import DamageEvaluationSerializer

class DamageEvaluationListView(generics.ListCreateAPIView):
    serializer_class = DamageEvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'tecnico':
            return DamageEvaluation.objects.filter(tecnico=user)
        return DamageEvaluation.objects.all()

    def perform_create(self, serializer):
        serializer.save(tecnico=self.request.user)

class DamageEvaluationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DamageEvaluation.objects.all()
    serializer_class = DamageEvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]
