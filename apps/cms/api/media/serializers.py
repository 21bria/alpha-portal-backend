from rest_framework import serializers

from apps.cms.models import (
    Media,
    MediaAlbum,
    MediaAlbumItem,
    MediaCategory,
)


class MediaCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaCategory
        fields = [
            "id",
            "name",
            "slug",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class MediaAlbumItemSerializer(serializers.ModelSerializer):
    media_title = serializers.CharField(source="media.title", read_only=True)
    media_file = serializers.FileField(source="media.file", read_only=True)

    class Meta:
        model = MediaAlbumItem
        fields = [
            "id",
            "media",
            "media_title",
            "media_file",
            "album",
            "position",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class MediaAlbumSerializer(serializers.ModelSerializer):
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
            "cover",
            "cover_url",
            "is_public",
            "total_items",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_by",
            "created_at",
            "updated_at",
        ]

    def get_cover_url(self, obj):
        request = self.context.get("request")

        cover_media = obj.cover

        if not cover_media:
            cover_media = obj.media_items.filter(type="IMAGE").first()

        if not cover_media:
            cover_media = obj.media_items.first()

        if not cover_media:
            return None

        if cover_media.thumbnail:
            url = cover_media.thumbnail.url
        elif cover_media.file:
            url = cover_media.file.url
        else:
            return None

        return request.build_absolute_uri(url) if request else url
    

class MediaSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()

    albums = serializers.PrimaryKeyRelatedField(
        queryset=MediaAlbum.objects.all(),
        many=True,
        required=False,
    )

    category_detail = MediaCategorySerializer(
        source="category",
        read_only=True,
    )

    albums_detail = MediaAlbumSerializer(
        source="albums",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Media
        fields = [
            "id",
            "title",
            "description",
            "type",
            "file",
            "file_url",
            "thumbnail",
            "thumbnail_url",
            "mime_type",
            "size",
            "width",
            "height",
            "duration",
            "alt_text",
            "caption",
            "is_public",
            "is_featured",
            "category",
            "category_detail",
            "albums",
            "albums_detail",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "file_url",
            "thumbnail_url",
            "mime_type",
            "size",
            "created_by",
            "created_at",
            "updated_at",
        ]

    def get_file_url(self, obj):
        request = self.context.get("request")

        if not obj.file:
            return None

        url = obj.file.url
        return request.build_absolute_uri(url) if request else url

    def get_thumbnail_url(self, obj):
        request = self.context.get("request")

        if not obj.thumbnail:
            return None

        url = obj.thumbnail.url
        return request.build_absolute_uri(url) if request else url

    def create(self, validated_data):
        albums = validated_data.pop("albums", [])

        request = self.context.get("request")
        file = validated_data.get("file")

        if file:
            validated_data["mime_type"] = getattr(file, "content_type", None)
            validated_data["size"] = getattr(file, "size", None)

        if request and request.user and request.user.is_authenticated:
            validated_data["created_by"] = request.user

        media = Media.objects.create(**validated_data)

        album_ids = []

        if albums:
            album_ids = [album.id for album in albums]

        elif request:
            album_ids = request.data.getlist("albums")

            if not album_ids:
                album_ids = request.data.getlist("albums[]")

            if not album_ids:
                album = request.data.get("albums")
                if album:
                    album_ids = [album]

        if album_ids:
            media.albums.set(album_ids)

        return media

    def update(self, instance, validated_data):
        albums = validated_data.pop("albums", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if albums is not None:
            instance.albums.set(albums)

        return instance