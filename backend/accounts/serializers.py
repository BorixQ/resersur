from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'telefono', 'direccion', 'rol',
            'dni_ruc', 'fecha_nacimiento',
            'codigo_empleado', 'area'
        ]
        
    def validate_password(self, value):
        validate_password(value)
        return value


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name',
            'password', 'password2',
            'telefono', 'direccion', 'rol',
            'dni_ruc', 'fecha_nacimiento',
            'codigo_empleado', 'area'
        ]

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        
        # Satisfacer el campo `username` requerido por AbstractUser
        username = validated_data.get('email')

        user = User.objects.create(
            username=username,
            **validated_data
        )
        user.set_password(password)
        user.save()
        return user
