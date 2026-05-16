from rest_framework import serializers
from apps.cms.models.projects import Project, ProjectSection


class PublicProjectSectionSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProjectSection
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


class PublicProjectSerializer(serializers.ModelSerializer):
    cover_image_url = serializers.SerializerMethodField()
    sections = PublicProjectSectionSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "slug",
            "subtitle",
            "description",
            "overview",
            "location",
            "province",
            "commodity",
            "status",
            "cover_image",
            "cover_image_url",
            "latitude",
            "longitude",
            "highlights",
            "seo_title",
            "seo_description",
            "sections",
        ]

    def get_cover_image_url(self, obj):
        request = self.context.get("request")
        if obj.cover_image and request:
            return request.build_absolute_uri(obj.cover_image.url)
        if obj.cover_image:
            return obj.cover_image.url
        return None