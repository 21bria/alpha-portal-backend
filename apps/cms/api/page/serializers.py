from rest_framework import serializers
from apps.cms.models import Page, PageSection

class PageSectionSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    page_detail = serializers.SerializerMethodField()

    class Meta:
        model = PageSection
        fields = [
            "id",
            "page",
            "page_detail",
            "section_type",
            "eyebrow",
            "title",
            "subtitle",
            "content",
            "image",
            "image_position",
            "image_url",
            "image_alt",
            "primary_button_text",
            "primary_button_url",
            "secondary_button_text",
            "secondary_button_url",
            "data",
            "sort_order",
            "is_active",
        ]

    def get_page_detail(self, obj):
        if not obj.page:
            return None

        return {
            "id": obj.page.id,
            "title": obj.page.title,
            "slug": obj.page.slug,
        }

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        if obj.image:
            return obj.image.url
        return None

class PageSerializer(serializers.ModelSerializer):
    sections = PageSectionSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = [
            "id",
            "title",
            "subtitle",
            "slug",
            "description",
            "is_published",
            "seo_title",
            "seo_description",
            "sections",
            "created_at",
            "updated_at",
        ]