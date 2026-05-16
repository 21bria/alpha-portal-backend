from rest_framework.generics import ListAPIView, RetrieveAPIView

from apps.cms.models import NewsTopic
from .serializers import PublicNewsTopicSerializer


class PublicNewsTopicListView(ListAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = PublicNewsTopicSerializer

    def get_queryset(self):
        return (
            NewsTopic.objects
            .select_related("category")
            .prefetch_related("tags")
            .filter(is_active=True)
            .order_by("sort_order", "title")
        )


class PublicNewsTopicDetailView(RetrieveAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = PublicNewsTopicSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return (
            NewsTopic.objects
            .select_related("category")
            .prefetch_related("tags")
            .filter(is_active=True)
        )