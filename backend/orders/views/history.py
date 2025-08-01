from rest_framework import generics, permissions
from orders.models.history import OTStatusHistory
from orders.serializers.history import OTStatusHistorySerializer

class OTStatusHistoryListView(generics.ListAPIView):
    serializer_class = OTStatusHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        ot_id = self.request.query_params.get('ot')
        if ot_id:
            return OTStatusHistory.objects.filter(ot_id=ot_id)
        return OTStatusHistory.objects.all()

class OTStatusHistoryDetailView(generics.RetrieveAPIView):
    queryset = OTStatusHistory.objects.all()
    serializer_class = OTStatusHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
