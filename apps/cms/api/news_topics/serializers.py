from rest_framework import serializers
from apps.cms.models.news import NewsTopic

class NewsTopicSerializer(serializers.ModelSerializer):
    category_detail = serializers.SerializerMethodField()
    tags_detail = serializers.SerializerMethodField()
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = NewsTopic
        fields = [
            "id",
            "title",
            "slug",
            "subtitle",
            "category",
            "category_detail",
            "tags",
            "tags_detail",
            "cover_image",
            "cover_image_url",
            "is_active",
            "sort_order",
        ]

    def get_category_detail(self, obj):
        if not obj.category:
            return None

        return {
            "id": obj.category.id,
            "name": obj.category.name,
            "slug": obj.category.slug,
        }

    def get_tags_detail(self, obj):
        return [
            {
                "id": tag.id,
                "name": tag.name,
                "slug": tag.slug,
            }
            for tag in obj.tags.all()
        ]

    def get_cover_image_url(self, obj):
        request = self.context.get("request")

        if obj.cover_image and request:
            return request.build_absolute_uri(obj.cover_image.url)

        if obj.cover_image:
            return obj.cover_image.url

        return None