from rest_framework import serializers

from apps.cms.models import CompanyProfile


class CompanyProfileSerializer(serializers.ModelSerializer):
    primary_logo_url = serializers.SerializerMethodField()
    white_logo_url   = serializers.SerializerMethodField()
    favicon_url      = serializers.SerializerMethodField()

    class Meta:
        model = CompanyProfile
        fields = [
            "id",
            "company_name",
            "legal_name",
            "tagline",
            "primary_logo",
            "primary_logo_url",
            "white_logo",
            "white_logo_url",
            "favicon",
            "favicon_url",
            "address",
            "phone",
            "email",
            "linkedin_url",
            "instagram_url",
            "youtube_url",
            "x_url",
            "copyright_text",
            "designer_name",
            "designer_url",
            "meta_title",
            "meta_description",
            "privacy_policy_url",
            "cookie_policy_url",
            "terms_url",
            "updated_at",
        ]
        read_only_fields = ["updated_at"]

    def get_primary_logo_url(self, obj):
        return self._file_url(obj.primary_logo)

    def get_white_logo_url(self, obj):
        return self._file_url(obj.white_logo)

    def get_favicon_url(self, obj):
        return self._file_url(obj.favicon)

    def _file_url(self, file):
        request = self.context.get("request")

        if file and request:
            return request.build_absolute_uri(file.url)

        if file:
            return file.url

        return None