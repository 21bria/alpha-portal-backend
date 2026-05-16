
from rest_framework.generics import ListAPIView, RetrieveAPIView
from apps.cms.api.pagination import StandardResultsSetPagination
from rest_framework import filters
from apps.cms.models.news import (
    NewsArticle,
    NewsCategory,
    NewsTag,
)

from .serializers import (
    PublicNewsArticleSerializer,
    PublicNewsCategorySerializer,
    PublicNewsTagSerializer,
)

class PublicNewsCategoryListView(ListAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = PublicNewsCategorySerializer

    def get_queryset(self):
        return NewsCategory.objects.all().order_by("name")


class PublicNewsTagListView(ListAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = PublicNewsTagSerializer

    def get_queryset(self):
        return NewsTag.objects.all().order_by("name")
    
class PublicNewsListView(ListAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = PublicNewsArticleSerializer

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "title",
        "excerpt",
        "content",
        "category__name",
        "tags__name",
    ]

    ordering_fields = [
        "published_at",
        "created_at",
        "title",
    ]

    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = (
            NewsArticle.objects
            .select_related("category")
            .prefetch_related("tags")
            .filter(status="published")
            .order_by("-published_at", "-created_at")
        )

        category = self.request.query_params.get("category")
        tag = self.request.query_params.get("tag")
        featured = self.request.query_params.get("featured")

        if category:
            qs = qs.filter(category__slug=category)

        if tag:
            qs = qs.filter(tags__slug=tag)

        if featured in ["1", "true", "yes"]:
            qs = qs.filter(is_featured=True)

        return qs.distinct()


class PublicNewsDetailView(RetrieveAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = PublicNewsArticleSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return (
            NewsArticle.objects
            .select_related("category")
            .prefetch_related("tags")
            .filter(status="published")
        )
    
