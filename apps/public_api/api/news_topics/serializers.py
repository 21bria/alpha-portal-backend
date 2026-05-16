from rest_framework import serializers
from apps.cms.models.news import NewsTopic

from ..news.serializers import PublicNewsCategorySerializer,PublicNewsTagSerializer

class PublicNewsTopicSerializer(serializers.ModelSerializer):
    category_detail = PublicNewsCategorySerializer(
        source="category",
        read_only=True,
    )

    tags_detail = PublicNewsTagSerializer(
        source="tags",
        many=True,
        read_only=True,
    )

    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = NewsTopic
        fields = [
            "id",
            "title",
            "slug",
            "subtitle",
            "category_detail",
            "tags_detail",
            "cover_image_url",
        ]

    def get_cover_image_url(self, obj):
        request = self.context.get("request")

        if obj.cover_image and request:
            return request.build_absolute_uri(obj.cover_image.url)

        if obj.cover_image:
            return obj.cover_image.url

        return None