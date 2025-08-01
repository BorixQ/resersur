from rest_framework import generics, permissions
from orders.models.photos import OTPhoto
from orders.serializers.photos import OTPhotoSerializer

class OTPhotoListView(generics.ListCreateAPIView):
    serializer_class = OTPhotoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'tecnico':
            return OTPhoto.objects.filter(tecnico=user)
        return OTPhoto.objects.all()

    def perform_create(self, serializer):
        serializer.save(tecnico=self.request.user)

class OTPhotoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OTPhoto.objects.all()
    serializer_class = OTPhotoSerializer
    permission_classes = [permissions.IsAuthenticated]
