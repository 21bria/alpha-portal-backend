from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from apps.cms.models import JobVacancy
from .serializers import JobVacancySerializer
from apps.cms.api.permissions import IsAuthenticatedOrReadOnlyCMS
from apps.cms.api.pagination import StandardResultsSetPagination


class JobVacancyViewSet(ModelViewSet):
    serializer_class = JobVacancySerializer
    permission_classes = [IsAuthenticatedOrReadOnlyCMS]
    pagination_class = StandardResultsSetPagination
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    lookup_field = "slug"

    search_fields = ["title","slug","department"]
    ordering_fields = ["created_at","title"]

    def get_queryset(self):
        qs = JobVacancy.objects.all()

        if self.request.method == "GET":
            qs = qs.filter(is_open=True)

        department = self.request.query_params.get("department")
        location = self.request.query_params.get("location")
        employment_type = self.request.query_params.get("employment_type")

        if department:
            qs = qs.filter(department__icontains=department)

        if location:
            qs = qs.filter(location__icontains=location)

        if employment_type:
            qs = qs.filter(employment_type__icontains=employment_type)

        return qs