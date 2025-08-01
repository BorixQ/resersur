# vehicles/serializers.py
from rest_framework import serializers
from .models import Vehicle
from django.contrib.auth import get_user_model

User = get_user_model()

class VehicleSerializer(serializers.ModelSerializer):
    cliente_dni_ruc = serializers.CharField(write_only=True, required=False)
    cliente = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Vehicle
        fields = ['id', 'marca', 'modelo', 'anio', 'placa', 'color', 'tipo', 'cliente', 'cliente_dni_ruc']
        extra_kwargs = {
            'marca': {'required': False},
            'modelo': {'required': False},
            'anio': {'required': False},
            'placa': {'required': False},
            'color': {'required': False},
            'tipo': {'required': False},
        }

    def get_cliente(self, obj):
        return {
            "id": obj.cliente.id,
            "email": obj.cliente.email,
            "dni_ruc": obj.cliente.dni_ruc,
            "nombre": f"{obj.cliente.first_name} {obj.cliente.last_name}"
        }

    def validate(self, data):
        user = self.context['request'].user

        # Validar cliente solo si el usuario NO es cliente
        if user.rol == 'cliente':
            if 'cliente_dni_ruc' in data:
                raise serializers.ValidationError({
                    "cliente_dni_ruc": "No puedes asignar este vehículo a otro cliente."
                })
        else:
            if 'cliente_dni_ruc' in data:
                try:
                    cliente = User.objects.get(dni_ruc=data['cliente_dni_ruc'], rol='cliente')
                    data['cliente_obj'] = cliente
                except User.DoesNotExist:
                    raise serializers.ValidationError({
                        "cliente_dni_ruc": "No se encontró un cliente con ese DNI/RUC."
                    })

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data.pop('cliente_dni_ruc', None)

        if user.rol == 'cliente':
            validated_data['cliente'] = user
        else:
            validated_data['cliente'] = validated_data.pop('cliente_obj')

        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        validated_data.pop('cliente_dni_ruc', None)

        if user.rol != 'cliente' and 'cliente_obj' in validated_data:
            instance.cliente = validated_data.pop('cliente_obj')

        # Evitar error si la placa no ha cambiado
        nueva_placa = validated_data.get('placa')
        if nueva_placa and nueva_placa == instance.placa:
            validated_data.pop('placa')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
