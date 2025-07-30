from django.urls import path
from accounts.views.roles import RolesListView, UserPermissionsView

urlpatterns = [
    path('roles/', RolesListView.as_view(), name='roles-list'),
    path('permissions/', UserPermissionsView.as_view(), name='user-permissions'),
]
