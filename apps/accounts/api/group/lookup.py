from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from apps.accounts.api.pagination import StandardResultsSetPagination 
from django.contrib.auth.models import Group, Permission
from apps.accounts.permissions import IsAuthenticatedOrReadOnlyCMS
from rest_framework import serializers
from django.contrib.auth.models import Group

class GroupLookupSerializer(serializers.ModelSerializer):
    value = serializers.CharField(source="id")
    label = serializers.CharField(source="name")

    class Meta:
        model = Group
        fields = ["value", "label"]


class GroupLookupViewSet(ReadOnlyModelViewSet):
    serializer_class = GroupLookupSerializer
    queryset = Group.objects.all().order_by("name")

    permission_classes = [IsAuthenticated, IsAuthenticatedOrReadOnlyCMS]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]