from rest_framework import generics, permissions
from orders.models.quotations import Quotation
from orders.serializers.quotations import QuotationSerializer

class QuotationListView(generics.ListCreateAPIView):
    serializer_class = QuotationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Quotation.objects.all()

class QuotationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer
    permission_classes = [permissions.IsAuthenticated]
