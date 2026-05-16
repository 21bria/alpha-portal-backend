from rest_framework import serializers
from apps.cms.models.documents import DocumentCategory, Document

class DocumentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentCategory
        fields = [
            "id",
            "name",
            "slug",
        ]


class DocumentSerializer(serializers.ModelSerializer):
    category_detail = DocumentCategorySerializer(source="category", read_only=True)

    file_url = serializers.SerializerMethodField()
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            "id",
            "category",
            "category_detail",
            "title",
            "slug",
            "description",
            "file",
            "file_url",
            "cover_image",
            "cover_image_url",
            "is_published",
            "published_at",
            "created_at",
        ]
        read_only_fields = [
            "slug",
            "created_at",
        ]

    def get_file_url(self, obj):
        request = self.context.get("request")

        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)

        if obj.file:
            return obj.file.url

        return None

    def get_cover_image_url(self, obj):
        request = self.context.get("request")

        if obj.cover_image and request:
            return request.build_absolute_uri(obj.cover_image.url)

        if obj.cover_image:
            return obj.cover_image.url

        return None