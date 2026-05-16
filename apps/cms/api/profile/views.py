from rest_framework import filters
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from apps.cms.models import CompanyProfile
from .serializers import CompanyProfileSerializer

from apps.cms.api.permissions import IsAuthenticatedOrReadOnlyCMS
from apps.cms.api.pagination import StandardResultsSetPagination

class CompanyProfileViewSet(ModelViewSet):
    serializer_class = CompanyProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnlyCMS]
    lookup_field = "id"
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    pagination_class = StandardResultsSetPagination

    search_fields = [
        "company_name",
        "legal_name",
        "email",
    ]

    ordering_fields = [
        "company_name",
        "updated_at",
    ]

    def get_queryset(self):
        return CompanyProfile.objects.all()

    def perform_create(self, serializer):
        if CompanyProfile.objects.exists():
            raise ValidationError({
                "detail": "Company profile already exists."
            })

        serializer.save()