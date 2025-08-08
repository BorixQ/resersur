from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied, ValidationError
from orders.models.quotations import Quotation
from orders.serializers.quotations import QuotationSerializer
from rest_framework.permissions import IsAuthenticated

class QuotationListCreateView(generics.ListCreateAPIView):
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.rol not in ['asesor', 'supervisor', 'admin']:
            raise PermissionDenied("No tienes permiso para crear cotizaciones.")

        ot = serializer.validated_data['ot']
        if serializer.validated_data.get('es_aprobada'):
            ya_aprobada = Quotation.objects.filter(ot=ot, es_aprobada=True).exists()
            if ya_aprobada:
                raise ValidationError("Ya existe una cotización aprobada para esta OT.")
        
        serializer.save(creado_por=user)

    def get_queryset(self):
        user = self.request.user

        if user.rol in ['admin', 'asesor', 'supervisor']:
            return Quotation.objects.all()

        if user.rol == 'cliente':
            return Quotation.objects.filter(ot__cliente=user)

        return Quotation.objects.none()

class QuotationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        user = self.request.user
        if user.rol not in ['asesor', 'supervisor', 'admin']:
            raise PermissionDenied("No tienes permiso para modificar cotizaciones.")

        instance = self.get_object()
        ot = instance.ot

        # Si se intenta marcar como aprobada
        if serializer.validated_data.get('es_aprobada') and not instance.es_aprobada:
            ya_aprobada = Quotation.objects.filter(ot=ot, es_aprobada=True).exclude(id=instance.id).exists()
            if ya_aprobada:
                raise ValidationError("Ya existe una cotización aprobada para esta OT.")

        serializer.save()
    
    def get_queryset(self):
        user = self.request.user

        if user.rol in ['admin', 'asesor', 'supervisor']:
            return Quotation.objects.all()

        if user.rol == 'cliente':
            return Quotation.objects.filter(ot__cliente=user)

        return Quotation.objects.none()
        

from django.http import FileResponse, Http404
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from orders.models.quotations import Quotation
import os

class QuotationPDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            quotation = Quotation.objects.get(pk=pk)

            if request.user.rol == 'cliente' and quotation.ot.cliente != request.user:
                return Response({"detail": "No tienes permiso para acceder a este documento."}, status=403)

            if request.user.rol not in ['admin', 'asesor', 'supervisor', 'cliente']:
                return Response({"detail": "No autorizado."}, status=403)

            file_path = quotation.documento.path

            if not os.path.exists(file_path):
                raise Http404("Archivo no encontrado.")

            return FileResponse(open(file_path, 'rb'), content_type='application/pdf')

        except Quotation.DoesNotExist:
            raise Http404("Cotización no encontrada.")
