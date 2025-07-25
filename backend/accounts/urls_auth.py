# accounts/urls_auth.py
from django.urls import path
from accounts.views.auth import (
    RegisterAPIView,
    EmailTokenObtainPairView,
    LogoutAPIView
)

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]
