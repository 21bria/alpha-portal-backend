# apps/cms/api/tasks/views.py

from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from apps.cms.models import Task
from apps.cms.api.pagination import StandardResultsSetPagination
from apps.cms.api.permissions import IsAuthenticatedOrReadOnlyCMS

from .serializers import TaskSerializer


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnlyCMS]
    lookup_field = "slug"
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = [
        "code",
        "title",
        "description",
        "location",
        "department",
        "assigned_to",
    ]

    ordering_fields = [
        "title",
        "status",
        "priority",
        "start_date",
        "due_date",
        "created_at",
        "updated_at",
    ]

    def get_queryset(self):
        qs = Task.objects.all()

        status = self.request.query_params.get("status")
        priority = self.request.query_params.get("priority")
        department = self.request.query_params.get("department")
        location = self.request.query_params.get("location")

        if status:
            qs = qs.filter(status=status)

        if priority:
            qs = qs.filter(priority=priority)

        if department:
            qs = qs.filter(department__iexact=department)

        if location:
            qs = qs.filter(location__icontains=location)

        return qs