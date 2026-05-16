from rest_framework import serializers
from apps.cms.models.news import NewsCategory, NewsTag, NewsArticle


class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ["id", "name", "slug"]


class NewsTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsTag
        fields = ["id", "name", "slug"]


class NewsArticleSerializer(serializers.ModelSerializer):
    category_detail = NewsCategorySerializer(source="category", read_only=True)

    tags = serializers.PrimaryKeyRelatedField(
        queryset=NewsTag.objects.all(),
        many=True,
        required=False,
    )
    tags_detail = NewsTagSerializer(source="tags", many=True, read_only=True)

    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = NewsArticle
        fields = [
            "id",
            "category",
            "category_detail",
            "tags",
            "tags_detail",
            "title",
            "slug",
            "excerpt",
            "content",
            "cover_image",
            "cover_image_url",
            "author_name",
            "published_at",
            "status",
            "is_featured",
            "allow_comments",
            "view_count",
            "reading_time",
            "seo_title",
            "seo_description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "slug",
            "view_count",
            "reading_time",
            "created_at",
            "updated_at",
        ]

    def get_cover_image_url(self, obj):
        request = self.context.get("request")
        if obj.cover_image and request:
            return request.build_absolute_uri(obj.cover_image.url)
        if obj.cover_image:
            return obj.cover_image.url
        return None