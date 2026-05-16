from django.contrib.auth.models import Group, Permission
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.accounts.permissions import IsAuthenticatedOrReadOnlyCMS

class GroupPermissionsView(APIView):
    permission_classes = [IsAuthenticated, IsAuthenticatedOrReadOnlyCMS]

    def get(self, request, pk):
        group = Group.objects.get(pk=pk)

        permissions = list(
            group.permissions.values_list("id", flat=True)
        )

        return Response({
            "group": group.name,
            "permissions": permissions
        })

    def patch(self, request, pk):
        group = Group.objects.get(pk=pk)

        permission_ids = request.data.get("permissions", [])

        perms = Permission.objects.filter(id__in=permission_ids)

        group.permissions.set(perms)

        return Response({
            "status": "updated"
        })