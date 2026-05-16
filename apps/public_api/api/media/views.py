from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.cms.models import (
    Media,
    MediaAlbum,
    MediaCategory,
)

from .serializers import (
    PublicMediaAlbumSerializer,
    PublicMediaCategorySerializer,
    PublicMediaSerializer,
)


class PublicMediaListView(generics.ListAPIView):
    serializer_class = PublicMediaSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = (
            Media.objects.filter(is_public=True)
            .select_related("category")
            .prefetch_related("albums")
            .order_by("-created_at")
        )

        media_type = self.request.query_params.get("type")
        category = self.request.query_params.get("category")
        album = self.request.query_params.get("album")
        featured = self.request.query_params.get("featured")

        if media_type:
            queryset = queryset.filter(type=media_type)

        if category:
            queryset = queryset.filter(category__slug=category)

        if album:
            queryset = queryset.filter(albums__slug=album)

        if featured in ["true", "1"]:
            queryset = queryset.filter(is_featured=True)

        return queryset.distinct()


class PublicMediaDetailView(generics.RetrieveAPIView):
    queryset = (
        Media.objects.filter(is_public=True)
        .select_related("category")
        .prefetch_related("albums")
    )

    serializer_class = PublicMediaSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"


class PublicMediaAlbumListView(generics.ListAPIView):
    serializer_class = PublicMediaAlbumSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            MediaAlbum.objects.filter(is_public=True)
            .select_related("cover")
            .prefetch_related("media_items")
            .order_by("-created_at")
        )


class PublicMediaAlbumDetailView(generics.RetrieveAPIView):
    queryset = (
        MediaAlbum.objects.filter(is_public=True)
        .select_related("cover")
        .prefetch_related("media_items")
    )

    serializer_class = PublicMediaAlbumSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"


class PublicMediaCategoryListView(generics.ListAPIView):
    queryset = MediaCategory.objects.all().order_by("name")
    serializer_class = PublicMediaCategorySerializer
    permission_classes = [AllowAny]