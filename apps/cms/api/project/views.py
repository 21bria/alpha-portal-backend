from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.cms.models.projects import Project, ProjectSection
from .serializers import ProjectSerializer, ProjectSectionSerializer

from apps.cms.api.permissions import IsAuthenticatedOrReadOnlyCMS
from apps.cms.api.pagination import StandardResultsSetPagination

class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnlyCMS]
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    pagination_class = StandardResultsSetPagination

    search_fields = [
        "title",
        "slug",
        "location",
        "province",
        "commodity",
        "status",
        "description",
        "overview",
    ]

    ordering_fields = [
        "title",
        "sort_order",
        "created_at",
        "updated_at",
        "status",
        "province",
        "commodity",
    ]

    def get_queryset(self):
        qs = Project.objects.prefetch_related("sections").all()

        if self.request.method == "GET":
            qs = qs.filter(is_published=True)

        status = self.request.query_params.get("status")
        province = self.request.query_params.get("province")
        commodity = self.request.query_params.get("commodity")

        if status:
            qs = qs.filter(status=status)

        if province:
            qs = qs.filter(province__icontains=province)

        if commodity:
            qs = qs.filter(commodity__icontains=commodity)

        return qs

    @action(detail=False, methods=["get"], url_path="by-slug/(?P<slug>[^/.]+)")
    def by_slug(self, request, slug=None):
        project = (
            self.get_queryset()
            .filter(slug=slug)
            .prefetch_related("sections")
            .first()
        )

        if not project:
            return Response({"detail": "Project not found."}, status=404)

        serializer = self.get_serializer(project)
        return Response(serializer.data)


class ProjectSectionViewSet(ModelViewSet):
    serializer_class = ProjectSectionSerializer
    permission_classes = [IsAuthenticatedOrReadOnlyCMS]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    pagination_class = StandardResultsSetPagination

    search_fields = [
        "project__title",
        "project__slug",
        "section_type",
        "title",
        "subtitle",
        "content",
    ]

    ordering_fields = [
        "project__title",
        "sort_order",
        "id",
        "title",
        "section_type",
    ]

    def get_queryset(self):
        qs = ProjectSection.objects.select_related("project").all()

        project_slug = self.request.query_params.get("project")
        section_type = self.request.query_params.get("section_type")

        if project_slug:
            qs = qs.filter(project__slug=project_slug)

        if section_type:
            qs = qs.filter(section_type=section_type)

        return qs.order_by("sort_order", "id")