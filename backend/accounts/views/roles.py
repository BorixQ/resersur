from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from accounts.constants import ROLES, PERMISOS_ROL

class RolesListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        roles = [{'key': key, 'value': value} for key, value in ROLES]
        return Response(roles)


class UserPermissionsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        rol = user.rol
        permisos = PERMISOS_ROL.get(rol, [])
        return Response({
            'rol': rol,
            'permissions': permisos
        })
