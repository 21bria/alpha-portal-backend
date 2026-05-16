from rest_framework import serializers
from apps.cms.models import Page, PageSection

class PublicPageSectionSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PageSection
        fields = [
            "id",
            "section_type",
            "eyebrow",
            "title",
            "subtitle",
            "content",
            "image",
            "image_url",
            "image_alt",
            "image_position",
            "primary_button_text",
            "primary_button_url",
            "secondary_button_text",
            "secondary_button_url",
            "data",
            "sort_order",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        if obj.image:
            return obj.image.url
        return None


class PublicPageSerializer(serializers.ModelSerializer):
    sections = PublicPageSectionSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = [
            "id",
            "title",
            "slug",
            "page_type",
            "subtitle",
            "description",
            "seo_title",
            "seo_description",
            "sections",
        ]
