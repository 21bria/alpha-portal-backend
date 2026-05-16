from rest_framework.viewsets import ModelViewSet

from apps.cms.models.documents import DocumentCategory, Document
from .serializers import DocumentCategorySerializer, DocumentSerializer
from apps.cms.api.permissions import IsAuthenticatedOrReadOnlyCMS
from apps.cms.api.pagination import StandardResultsSetPagination


class DocumentCategoryViewSet(ModelViewSet):
    serializer_class = DocumentCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnlyCMS]
    pagination_class = StandardResultsSetPagination
    lookup_field = "slug"

    def get_queryset(self):
        return DocumentCategory.objects.all().order_by("name")


class DocumentViewSet(ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticatedOrReadOnlyCMS]
    pagination_class = StandardResultsSetPagination
    lookup_field = "slug"

    def get_queryset(self):
        qs = Document.objects.select_related("category").all()

        if self.request.method == "GET":
            qs = qs.filter(is_published=True)

        category = self.request.query_params.get("category")

        if category:
            qs = qs.filter(category__slug=category)

        return qs