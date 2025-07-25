# accounts/urls_profile.py
from django.urls import path
from accounts.views.profile import UserProfileView, ChangePasswordView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
