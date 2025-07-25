from rest_framework import status, permissions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.serializers import UserCreateSerializer


class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar campo 'email' en vez de 'username'
        self.fields['email'] = serializers.EmailField()
        self.fields['password'] = serializers.CharField()
        if 'username' in self.fields:
            self.fields.pop('username')

    def validate(self, attrs):
        # Hacer que el campo 'email' actúe como 'username' internamente
        attrs['username'] = attrs.get('email')
        return super().validate(attrs)


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout exitoso."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Token inválido o expirado."}, status=status.HTTP_400_BAD_REQUEST)
