from rest_framework import serializers
from apps.cms.models.news import NewsArticle, NewsCategory, NewsTag


class PublicNewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ["id", "name", "slug"]


class PublicNewsTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsTag
        fields = ["id", "name", "slug"]


class PublicNewsArticleSerializer(serializers.ModelSerializer):
    category_detail = PublicNewsCategorySerializer(source="category", read_only=True)
    tags_detail = PublicNewsTagSerializer(source="tags", many=True, read_only=True)
    cover_image_url = serializers.SerializerMethodField()
    cover_thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = NewsArticle
        fields = [
            "id",
            "category_detail",
            "tags_detail",
            "title",
            "slug",
            "excerpt",
            "content",
            "cover_image_url",
            "cover_thumbnail_url",
            "author_name",
            "published_at",
            "is_featured",
            "reading_time",
            "seo_title",
            "seo_description",
        ]

    def get_cover_image_url(self, obj):
        request = self.context.get("request")
        if obj.cover_image and request:
            return request.build_absolute_uri(obj.cover_image.url)
        if obj.cover_image:
            return obj.cover_image.url
        return None

    def get_cover_thumbnail_url(self, obj):
        request = self.context.get("request")
        if getattr(obj, "cover_thumbnail", None) and request:
            return request.build_absolute_uri(obj.cover_thumbnail.url)
        if getattr(obj, "cover_thumbnail", None):
            return obj.cover_thumbnail.url
        return None