from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from apps.cms.api.pagination import StandardResultsSetPagination

from apps.cms.models import (
    Media,
    MediaAlbum,
    MediaAlbumItem,
    MediaCategory,
)

from .serializers import (
    MediaAlbumItemSerializer,
    MediaAlbumSerializer,
    MediaCategorySerializer,
    MediaSerializer,
)


class IsAuthenticatedOrPublicReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["public", "list", "retrieve"]:
            return True

        return request.user and request.user.is_authenticated


class MediaCategoryViewSet(viewsets.ModelViewSet):
    queryset = MediaCategory.objects.all()
    serializer_class = MediaCategorySerializer
    permission_classes = [IsAuthenticatedOrPublicReadOnly]
    pagination_class = StandardResultsSetPagination
    lookup_field = "slug"


class MediaAlbumViewSet(viewsets.ModelViewSet):
    queryset = MediaAlbum.objects.select_related(
        "cover",
        "created_by",
    ).prefetch_related("media_items")
    serializer_class = MediaAlbumSerializer
    permission_classes = [IsAuthenticatedOrPublicReadOnly]
    pagination_class = StandardResultsSetPagination
    lookup_field = "slug"

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=["get"])
    def public(self, request):
        queryset = self.get_queryset().filter(is_public=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.select_related(
        "category",
        "created_by",
    ).prefetch_related("albums")
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticatedOrPublicReadOnly]
    pagination_class = StandardResultsSetPagination
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        queryset = super().get_queryset()

        media_type = self.request.query_params.get("type")
        category = self.request.query_params.get("category")
        album = self.request.query_params.get("album")
        is_featured = self.request.query_params.get("is_featured")

        if media_type:
            queryset = queryset.filter(type=media_type)

        if category:
            queryset = queryset.filter(category__slug=category)

        if album:
            queryset = queryset.filter(albums__slug=album)

        if is_featured in ["true", "1"]:
            queryset = queryset.filter(is_featured=True)

        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=["get"])
    def public(self, request):
        queryset = self.get_queryset().filter(is_public=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MediaAlbumItemViewSet(viewsets.ModelViewSet):
    queryset = MediaAlbumItem.objects.select_related(
        "media",
        "album",
    )
    serializer_class = MediaAlbumItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination