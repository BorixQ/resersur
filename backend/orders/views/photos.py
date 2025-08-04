from rest_framework import generics, permissions
from orders.models.photos import OTPhoto
from orders.serializers.photos import OTPhotoSerializer
from rest_framework.exceptions import PermissionDenied

class OTPhotoListCreateView(generics.ListCreateAPIView):
    serializer_class = OTPhotoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'cliente':
            return OTPhoto.objects.none()
        return OTPhoto.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        if user.rol not in ['asesor', 'supervisor', 'admin', 'tecnico']:
            raise PermissionDenied("No tienes permiso para subir fotos.")
        serializer.save(usuario=user)

class OTPhotoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OTPhoto.objects.all()
    serializer_class = OTPhotoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if user.rol == 'cliente':
            raise PermissionDenied("No puedes acceder a fotos.")
        return obj
