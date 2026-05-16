from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters

from apps.cms.models.news import NewsCategory, NewsTag, NewsArticle

from apps.cms.api.news.serializers import (
    NewsCategorySerializer,
    NewsTagSerializer,
    NewsArticleSerializer,
)
from apps.cms.api.permissions import IsAuthenticatedOrReadOnlyCMS
from apps.cms.api.pagination import StandardResultsSetPagination


class NewsCategoryViewSet(ModelViewSet):
    serializer_class = NewsCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnlyCMS]
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    pagination_class = StandardResultsSetPagination
    lookup_field = "slug"

    search_fields = ["name"]
    ordering_fields = ["created_at","name"]


    def get_queryset(self):
        return NewsCategory.objects.all().order_by("name")

class NewsTagViewSet(ModelViewSet):
    serializer_class = NewsTagSerializer
    permission_classes = [IsAuthenticatedOrReadOnlyCMS]
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    pagination_class = StandardResultsSetPagination
    lookup_field = "slug"

    search_fields = ["name"]
    ordering_fields = ["created_at","name"]

    def get_queryset(self):
        return NewsTag.objects.all().order_by("name")
    
class NewsArticleViewSet(ModelViewSet):
    serializer_class = NewsArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnlyCMS]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    pagination_class = StandardResultsSetPagination
    lookup_field = "slug"

    search_fields = ["title", "excerpt", "content", "category__name", "tags__name"]
    ordering_fields = ["created_at", "updated_at", "published_at", "title"]
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = NewsArticle.objects.select_related("category").prefetch_related("tags").all()

        if self.request.method == "GET" and not self.request.user.is_authenticated:
            qs = qs.filter(status="published")

        category = self.request.query_params.get("category")
        tag = self.request.query_params.get("tag")
        featured = self.request.query_params.get("featured")
        status = self.request.query_params.get("status")

        if category:
            qs = qs.filter(category__slug=category)

        if tag:
            qs = qs.filter(tags__slug=tag)

        if featured in ["true", "1", "yes"]:
            qs = qs.filter(is_featured=True)

        if status:
            qs = qs.filter(status=status)

        return qs.distinct()

    
    @action(detail=False, methods=["get"], url_path="by-slug/(?P<slug>[^/.]+)")
    def by_slug(self, request, slug=None):
        article = self.get_queryset().filter(slug=slug).first()

        if not article:
            return Response({"detail": "Article not found."}, status=404)

        serializer = self.get_serializer(article)
        return Response(serializer.data)