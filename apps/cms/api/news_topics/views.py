from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from apps.cms.models import NewsTopic
from .serializers import NewsTopicSerializer
from apps.cms.api.permissions import IsAuthenticatedOrReadOnlyCMS
from apps.cms.api.pagination import StandardResultsSetPagination

class NewsTopicViewSet(ModelViewSet):
    serializer_class = NewsTopicSerializer
    permission_classes = [IsAuthenticatedOrReadOnlyCMS]
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    pagination_class = StandardResultsSetPagination

    lookup_field = "slug"

    search_fields = ["title","slug"]
    ordering_fields = ["created_at","title"]

    def get_queryset(self):
        return (
            NewsTopic.objects
            .select_related("category")
            .prefetch_related("tags")
            .all()
        )