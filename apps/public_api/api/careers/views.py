# apps/cms/api/public/careers/views.py

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import filters

from apps.cms.models import JobVacancy
from apps.public_api.api.pagination import StandardResultsSetPagination

from .serializers import PublicJobVacancySerializer


class PublicJobVacancyListView(ListAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = PublicJobVacancySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = [
        "title",
        "department",
        "location",
        "employment_type",
        "summary",
    ]

    ordering_fields = [
        "published_at",
        "created_at",
        "title",
        "department",
    ]

    def get_queryset(self):
        qs = (
            JobVacancy.objects
            .filter(is_open=True)
            .order_by("-published_at", "-created_at")
        )

        department = self.request.query_params.get("department")
        location = self.request.query_params.get("location")
        employment_type = self.request.query_params.get("employment_type")

        if department:
            qs = qs.filter(department__iexact=department)

        if location:
            qs = qs.filter(location__icontains=location)

        if employment_type:
            qs = qs.filter(employment_type__iexact=employment_type)

        return qs


class PublicJobVacancyDetailView(RetrieveAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = PublicJobVacancySerializer
    lookup_field = "slug"

    def get_queryset(self):
        return JobVacancy.objects.filter(is_open=True)