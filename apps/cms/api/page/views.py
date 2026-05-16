from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from apps.cms.models import Page, PageSection
from .serializers import PageSerializer, PageSectionSerializer
from apps.cms.api.permissions import IsAuthenticatedOrReadOnlyCMS
from apps.cms.api.pagination import StandardResultsSetPagination

class PageViewSet(ModelViewSet):
    serializer_class = PageSerializer
    permission_classes = [IsAuthenticatedOrReadOnlyCMS]
    lookup_field = "slug"
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    pagination_class = StandardResultsSetPagination

    search_fields = ["title","slug"]
    ordering_fields = ["created_at","title"]

    def get_queryset(self):
        qs = Page.objects.prefetch_related("sections").all()

        if self.request.method == "GET":
            qs = qs.filter(is_published=True)

        return qs

    @action(detail=False, methods=["get"], url_path="by-slug/(?P<slug>[^/.]+)")
    def by_slug(self, request, slug=None):
        page = (
            self.get_queryset()
            .filter(slug=slug)
            .prefetch_related("sections")
            .first()
        )

        if not page:
            return Response({"detail": "Page not found."}, status=404)

        serializer = self.get_serializer(page)
        return Response(serializer.data)


class PageSectionViewSet(ModelViewSet):
    serializer_class = PageSectionSerializer
    permission_classes = [IsAuthenticatedOrReadOnlyCMS]
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "page__title",
        "page__slug",
        "section_type",
        "title",
        "subtitle",
    ]
    ordering_fields = [
        "page__title",
        "sort_order",
        "id",
        "title",
        "section_type",
    ]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = PageSection.objects.select_related("page").all()

        print("USER:", self.request.user)
        print("COUNT:", qs.count())

        # page_slug = self.request.query_params.get("page")
        section_type = self.request.query_params.get("section_type")

        # if page_slug:
        #     qs = qs.filter(page__slug=page_slug)

        if section_type:
            qs = qs.filter(section_type=section_type)

        return qs.order_by("sort_order", "id")