# accounts/urls.py
from django.urls import path, include
from accounts.views.auth import RegisterAPIView, EmailTokenObtainPairView, LogoutAPIView


urlpatterns = [
    path('auth/', include('accounts.urls_auth')),  # Ahora es /api/accounts/auth/
]
