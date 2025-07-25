from django.urls import path
from accounts.views.users import UserListView, UserDetailView

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('<int:id>/', UserDetailView.as_view(), name='user-detail'),
]
