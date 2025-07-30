# accounts/urls.py
from django.urls import path, include
from accounts.views.auth import RegisterAPIView, EmailTokenObtainPairView, LogoutAPIView


urlpatterns = [
    path('auth/', include('accounts.urls_auth')),  # Ahora es /api/accounts/auth/
    path('users/', include('accounts.urls_users')),  # Ahora es /api/accounts/users/
    path('', include('accounts.urls_profile')),
    path('', include('accounts.urls_roles')),
]
