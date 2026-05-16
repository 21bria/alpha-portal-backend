from rest_framework import serializers
from apps.cms.models.projects import Project, ProjectSection


class ProjectSectionSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    project_detail = serializers.SerializerMethodField()

    class Meta:
        model = ProjectSection
        fields = [
            "id",
            "project",
            "project_detail",
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

    def get_project_detail(self, obj):
        if not obj.project:
            return None

        return {
            "id": obj.project.id,
            "title": obj.project.title,
            "slug": obj.project.slug,
        }

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        if obj.image:
            return obj.image.url
        return None


class ProjectSerializer(serializers.ModelSerializer):
    cover_image_url = serializers.SerializerMethodField()
    sections = ProjectSectionSerializer(many=True, read_only=True)

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
            "is_published",
            "sort_order",
            "sections",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["slug", "created_at", "updated_at"]

    def get_cover_image_url(self, obj):
        request = self.context.get("request")
        if obj.cover_image and request:
            return request.build_absolute_uri(obj.cover_image.url)
        if obj.cover_image:
            return obj.cover_image.url
        return None