from rest_framework import generics, permissions
from orders.models.history import OTStatusHistory
from orders.serializers.history import OTStatusHistorySerializer

class OTStatusHistoryListView(generics.ListAPIView):
    serializer_class = OTStatusHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        ot_id = self.request.query_params.get('ot')
        qs = OTStatusHistory.objects.all()
        if ot_id:
            qs = qs.filter(ot_id=ot_id)
        if self.request.user.rol == 'cliente':
            qs = qs.filter(ot__cliente=self.request.user)
        return qs.order_by('-fecha_cambio')

class OTStatusHistoryDetailView(generics.RetrieveAPIView):
    queryset = OTStatusHistory.objects.all()
    serializer_class = OTStatusHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
