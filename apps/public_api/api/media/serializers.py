from rest_framework import serializers

from apps.cms.models import (
    Media,
    MediaAlbum,
    MediaCategory,
)


class PublicMediaCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaCategory
        fields = [
            "id",
            "name",
            "slug",
        ]


class PublicMediaAlbumSerializer(serializers.ModelSerializer):
    cover_url = serializers.SerializerMethodField()
    total_items = serializers.IntegerField(
        source="media_items.count",
        read_only=True,
    )

    class Meta:
        model = MediaAlbum
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "cover_url",
            "total_items",
        ]

    def get_cover_url(self, obj):
        request = self.context.get("request")

        cover_media = obj.cover

        if not cover_media:
            cover_media = obj.media_items.filter(
                is_public=True,
                type="IMAGE",
            ).first()

        if not cover_media:
            return None

        if cover_media.thumbnail:
            url = cover_media.thumbnail.url
        elif cover_media.file:
            url = cover_media.file.url
        else:
            return None

        return request.build_absolute_uri(url) if request else url


class PublicMediaSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()

    category = PublicMediaCategorySerializer(read_only=True)
    albums = PublicMediaAlbumSerializer(many=True, read_only=True)

    class Meta:
        model = Media
        fields = [
            "id",
            "title",
            "description",
            "type",
            "file_url",
            "thumbnail_url",
            "width",
            "height",
            "duration",
            "alt_text",
            "caption",
            "is_featured",
            "category",
            "albums",
            "created_at",
        ]

    def get_file_url(self, obj):
        request = self.context.get("request")

        if not obj.file:
            return None

        url = obj.file.url
        return request.build_absolute_uri(url) if request else url

    def get_thumbnail_url(self, obj):
        request = self.context.get("request")

        if obj.thumbnail:
            url = obj.thumbnail.url
        elif obj.file:
            url = obj.file.url
        else:
            return None

        return request.build_absolute_uri(url) if request else url