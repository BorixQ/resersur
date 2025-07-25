# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes
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
    
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        User = get_user_model()
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No existe un usuario con este email.")
        return value

    def save(self):
        User = get_user_model()
        user = User.objects.get(email=self.validated_data['email'])

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        return {
            "uid": uid,
            "token": token
        }

class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return data

    def save(self):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(self.validated_data['uid']))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            raise serializers.ValidationError("Token o UID inválido.")

        if not default_token_generator.check_token(user, self.validated_data['token']):
            raise serializers.ValidationError("Token inválido o expirado.")

        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
    
class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'  # o define campos específicos si prefieres mayor control
        read_only_fields = ['id', 'email', 'username', 'last_login', 'date_joined']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value