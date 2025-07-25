from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator

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
            is_active=False,
            **validated_data
        )
        user.set_password(password)
        user.save()
        return user

class EmailVerificationSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data['uid']))
            user = get_user_model().objects.get(pk=uid)
        except Exception:
            raise serializers.ValidationError("UID inválido.")

        if not default_token_generator.check_token(user, data['token']):
            raise serializers.ValidationError("Token inválido o expirado.")

        data['user'] = user
        return data

    def save(self):
        user = self.validated_data['user']
        user.is_active = True
        user.save()
        return user